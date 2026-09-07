import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from math import log, pi, sqrt
from matplotlib.backends.backend_pdf import PdfPages

# Simulation parameters for Mars EDL Doppler tracking
#====================================================
# Parameters based on Mars EDL communications scenario from the paper
M       = 4     # System order (number of taps)
L       = 100   # Realizations
N       = 10000 # Time iterations (increased for better convergence)
mu      = 1e-3  # ε-NLMS Step size
mu_ga_complex = 1e-3  # GA-LMS Complex Step size
mu_ga_rotors = 1e-4   # GA-LMS Rotors Step size
sigma2v = 1e-2  # Variance of measurement noise
Fs      = 100   # Sampling frequency (Hz)

# Mars EDL Doppler profile parameters (scaled for 10k samples)
f0 = 0          # Nominal frequency (after down-conversion)
acceleration_peak_time = 2000   # Time of acceleration peak (sample index)
parachute_time = 6000          # Time of parachute deployment (sample index)

BINARY_COMPLEX = '../../src/GAAFs_doppler/doppler_galms_complex/build/doppler_galms_complex'  # Complex GA-LMS binary
BINARY_ROTORS = '../../src/GAAFs_doppler/doppler_galms_rotors/build/doppler_galms_rotors'  # Quaternion rotors GA-LMS binary
#====================================================

def generate_mars_edl_doppler_profile(N):
    """
    Generate a challenging Doppler frequency profile with prominent effects and discontinuities
    to stress-test adaptive filter tracking capabilities
    """
    # Time vector (sample indices)
    t = np.arange(N)

    # Initialize frequency profile
    f_doppler = np.zeros(N)

    # Phase 1: Initial descent (samples 0 to 1000) - rapid frequency sweep from -80 Hz to +120 Hz
    phase1_end = 1000
    phase1_mask = t < phase1_end
    phase1_progress = t[phase1_mask] / phase1_end
    # Aggressive frequency sweep with oscillations
    f_doppler[phase1_mask] = -80 + 200 * phase1_progress + 20 * np.sin(8 * pi * phase1_progress)

    # DISCONTINUITY 1: Sudden jump at sample 1000
    # Phase 2: Acceleration shock (samples 1000 to 1500) - step jump to -150 Hz then rapid rise
    phase2_start = 1000
    phase2_end = 1500
    phase2_mask = (t >= phase2_start) & (t < phase2_end)
    phase2_progress = (t[phase2_mask] - phase2_start) / (phase2_end - phase2_start)
    # Step discontinuity followed by exponential rise
    f_doppler[phase2_mask] = -150 + 250 * (1 - np.exp(-5 * phase2_progress))

    # Phase 3: High-dynamic oscillations (samples 1500 to 3000) - extreme frequency variations
    phase3_start = 1500
    phase3_end = 3000
    phase3_mask = (t >= phase3_start) & (t < phase3_end)
    phase3_progress = (t[phase3_mask] - phase3_start) / (phase3_end - phase3_start)
    # Multiple frequency components with rapid changes
    base_freq = 50 * np.sin(2 * pi * phase3_progress)
    fast_osc = 80 * np.sin(20 * pi * phase3_progress) * np.exp(-2 * phase3_progress)
    chirp = 40 * np.sin(pi * phase3_progress**2 * 10)
    f_doppler[phase3_mask] = base_freq + fast_osc + chirp

    # DISCONTINUITY 2: Another step jump at sample 3000
    # Phase 4: Extreme acceleration (samples 3000 to 3500) - step to +180 Hz
    phase4_start = 3000
    phase4_end = 3500
    phase4_mask = (t >= phase4_start) & (t < phase4_end)
    phase4_progress = (t[phase4_mask] - phase4_start) / (phase4_end - phase4_start)
    # High frequency with modulation
    f_doppler[phase4_mask] = 180 + 30 * np.sin(12 * pi * phase4_progress) * (1 - phase4_progress)

    # Phase 5: Chaotic dynamics (samples 3500 to 5500) - complex multi-component signal
    phase5_start = 3500
    phase5_end = 5500
    phase5_mask = (t >= phase5_start) & (t < phase5_end)
    phase5_progress = (t[phase5_mask] - phase5_start) / (phase5_end - phase5_start)
    # Combination of multiple sinusoids with different rates
    comp1 = 60 * np.sin(3 * pi * phase5_progress)
    comp2 = 40 * np.sin(7 * pi * phase5_progress + pi/4)
    comp3 = 25 * np.sin(15 * pi * phase5_progress + pi/2)
    trend = -120 * phase5_progress  # Overall downward trend
    f_doppler[phase5_mask] = 120 + comp1 + comp2 + comp3 + trend

    # DISCONTINUITY 3: Parachute deployment shock at sample 5500
    # Phase 6: Parachute deployment (samples 5500 to 6000) - sudden drop to -200 Hz
    phase6_start = 5500
    phase6_end = 6000
    phase6_mask = (t >= phase6_start) & (t < phase6_end)
    phase6_progress = (t[phase6_mask] - phase6_start) / (phase6_end - phase6_start)
    # Sharp step down with damped oscillations
    f_doppler[phase6_mask] = -200 + 50 * np.sin(10 * pi * phase6_progress) * np.exp(-8 * phase6_progress)

    # Phase 7: Recovery and stabilization (samples 6000 to 7000) - rapid frequency sweeps
    phase7_start = 6000
    phase7_end = 7000
    phase7_mask = (t >= phase7_start) & (t < phase7_end)
    phase7_progress = (t[phase7_mask] - phase7_start) / (phase7_end - phase7_start)
    # Frequency sweeps with decreasing amplitude
    sweep1 = 100 * np.sin(pi * phase7_progress**2 * 8) * (1 - phase7_progress)
    sweep2 = 50 * np.sin(pi * (1-phase7_progress)**2 * 6)
    f_doppler[phase7_mask] = -80 + sweep1 + sweep2

    # DISCONTINUITY 4: Final approach shock at sample 7000
    # Phase 8: Final approach (samples 7000 to end) - step to positive then exponential decay
    phase8_start = 7000
    phase8_mask = t >= phase8_start
    phase8_progress = (t[phase8_mask] - phase8_start) / (N - phase8_start)
    # Step up then exponential decay with residual oscillations
    step_component = 80 * np.exp(-6 * phase8_progress)
    oscillation = 15 * np.sin(4 * pi * phase8_progress) * np.exp(-4 * phase8_progress)
    final_trend = -30 * (1 - np.exp(-3 * phase8_progress))
    f_doppler[phase8_mask] = step_component + oscillation + final_trend

    return f_doppler

def generate_signal_samples(N, f_doppler, Fs, sigma2v):
    """
    Generate the complex signal x(i) = exp(j*omega*i) + v(i)
    where omega is the discrete time-varying Doppler component
    """
    # Convert frequency to discrete angular frequency
    omega = 2 * pi * f_doppler / Fs
    
    # Generate phase by integrating frequency (cumulative sum)
    # This creates the time-varying phase trajectory
    dt = 1.0 / Fs
    phase = np.cumsum(omega) * dt
    
    # Generate the complex exponential signal
    x_clean = np.exp(1j * phase)
    
    # Add complex white Gaussian noise
    noise_real = np.random.normal(0, sqrt(sigma2v/2), N)
    noise_imag = np.random.normal(0, sqrt(sigma2v/2), N)
    noise = noise_real + 1j * noise_imag
    
    x_noisy = x_clean + noise
    
    return x_clean, x_noisy, omega, phase

class EpsilonNLMS:
    """
    Epsilon-Normalized Least Mean Squares adaptive filter
    Based on the linear prediction approach from the Mars communications paper
    """

    def __init__(self, M, mu, epsilon=1e-5):
        """
        Initialize ε-NLMS filter

        Args:
            M: Filter order (number of taps)
            mu: Step size
            epsilon: Regularization parameter
        """
        self.M = M
        self.mu = mu
        self.epsilon = epsilon

        # Initialize filter coefficients (complex-valued)
        self.coeffs = np.zeros(M, dtype=complex)

        # Initialize input buffer
        self.x_buffer = np.zeros(M, dtype=complex)

        # Storage for outputs and errors
        self.outputs = []
        self.errors = []
        self.emse_values = []  # Store EMSE values
        
    def update(self, x_input):
        """
        Update filter with new input sample
        
        Args:
            x_input: New complex input sample
            
        Returns:
            y_output: Filter output (prediction)
            error: Prediction error
        """
        # Shift buffer and add new sample
        self.x_buffer[1:] = self.x_buffer[:-1]
        self.x_buffer[0] = x_input
        
        # Calculate filter output (prediction of current sample using past samples)
        y_output = np.dot(self.coeffs, self.x_buffer)
        
        # Calculate prediction error
        error = x_input - y_output
        
        # Update coefficients using ε-NLMS rule
        # c_i = c_{i-1} + μ * x*_{i-1} / (||x_{i-1}||^2 + ε) * e(i)
        power = np.real(np.dot(np.conj(self.x_buffer), self.x_buffer))
        normalized_step = self.mu / (power + self.epsilon)
        
        # Update coefficients
        self.coeffs += normalized_step * np.conj(self.x_buffer) * error
        
        # Store outputs and errors
        self.outputs.append(y_output)
        self.errors.append(error)
        
        return y_output, error
    
    def update_with_emse(self, x_input, x_clean=None):
        """
        Update filter with new input sample and calculate EMSE

        Args:
            x_input: New complex input sample (noisy)
            x_clean: Clean input sample (for EMSE calculation)

        Returns:
            y_output: Filter output (prediction)
            error: Prediction error
            emse: Excess mean square error (estimation component only)
        """
        # Shift buffer and add new sample
        self.x_buffer[1:] = self.x_buffer[:-1]
        self.x_buffer[0] = x_input

        # Calculate filter output (prediction of current sample using past samples)
        y_output = np.dot(self.coeffs, self.x_buffer)

        # Calculate prediction error
        error = x_input - y_output

        # Calculate EMSE if clean signal is provided
        emse = 0.0
        if x_clean is not None:
            # EMSE = |x_clean - y_output|^2
            # This is the estimation error component without external noise
            estimation_error = x_clean - y_output
            emse = np.real(estimation_error * np.conj(estimation_error))

        # Update coefficients using ε-NLMS rule
        power = np.real(np.dot(np.conj(self.x_buffer), self.x_buffer))
        normalized_step = self.mu / (power + self.epsilon)

        # Update coefficients
        self.coeffs += normalized_step * np.conj(self.x_buffer) * error

        # Store outputs, errors, and EMSE
        self.outputs.append(y_output)
        self.errors.append(error)
        self.emse_values.append(emse)

        return y_output, error, emse

    def process_signal(self, x_signal):
        """
        Process entire signal through the filter

        Args:
            x_signal: Complex input signal array

        Returns:
            outputs: Array of filter outputs
            errors: Array of prediction errors
        """
        outputs = np.zeros_like(x_signal)
        errors = np.zeros_like(x_signal)

        for i, x in enumerate(x_signal):
            y, e = self.update(x)
            outputs[i] = y
            errors[i] = e

        return outputs, errors

    def process_signal_with_emse(self, x_signal, x_clean_signal):
        """
        Process entire signal through the filter with EMSE calculation

        Args:
            x_signal: Complex noisy input signal array
            x_clean_signal: Complex clean reference signal array

        Returns:
            outputs: Array of filter outputs
            errors: Array of prediction errors
            emse_array: Array of EMSE values
        """
        outputs = np.zeros_like(x_signal)
        errors = np.zeros_like(x_signal)
        emse_array = np.zeros(len(x_signal), dtype=float)

        for i, (x_noisy, x_clean) in enumerate(zip(x_signal, x_clean_signal)):
            y, e, emse = self.update_with_emse(x_noisy, x_clean)
            outputs[i] = y
            errors[i] = e
            emse_array[i] = emse

        return outputs, errors, emse_array

def save_signal_to_file(x_signal, filename):
    """
    Save complex signal to file in the format expected by C++ code
    Real part in first column, imaginary part in second column
    """
    with open(filename, 'w') as f:
        for sample in x_signal:
            f.write("{} {}\n".format(sample.real, sample.imag))

def load_signal_from_file(filename):
    """
    Load complex signal from file output by C++ code
    """
    try:
        data = np.loadtxt(filename)
        if data.shape[1] == 2:
            return data[:, 0] + 1j * data[:, 1]
        else:
            return data[:, 0]  # Real-valued data
    except:
        return np.array([])

def load_scalar_from_file(filename):
    """
    Load a single scalar value from file
    """
    try:
        with open(filename, 'r') as f:
            return float(f.readline().strip())
    except:
        return 0.0

# Create multipage PDF for results
pp = PdfPages('mars_edl_signal_tracking_comparison.pdf')

print("Generating Mars EDL Doppler profile...")

# Generate the exact Doppler frequency profile from the paper
f_doppler_true = generate_mars_edl_doppler_profile(N)

# Generate signal samples for each realization
print("Generating signal realizations...")
all_x_clean = []
all_x_noisy = []
all_omega = []

for realization in range(L):
    print("Generating realization {} of {}".format(realization + 1, L))
    
    # Add some variability between realizations (small perturbations)
    f_doppler_real = f_doppler_true + np.random.normal(0, 0.5, N)  # Small variations
    
    x_clean, x_noisy, omega, phase = generate_signal_samples(N, f_doppler_real, Fs, sigma2v)
    
    all_x_clean.append(x_clean)
    all_x_noisy.append(x_noisy)
    all_omega.append(omega)
    
    # Save this realization's input signal
    save_signal_to_file(x_noisy, 'input_signal_real_{}.txt'.format(realization))

# Save average input signal for C++ processing
avg_x_noisy = np.mean(all_x_noisy, axis=0)
avg_x_clean = np.mean(all_x_clean, axis=0)
save_signal_to_file(avg_x_noisy, 'input_signal.txt')

print("Processing with e-NLMS adaptive filter...")

# Process signal with e-NLMS including EMSE calculation
epsilon_nlms = EpsilonNLMS(M=M, mu=mu, epsilon=1e-5)
x_estimated_nlms, errors_nlms, emse_nlms = epsilon_nlms.process_signal_with_emse(avg_x_noisy, avg_x_clean)

# Calculate MSE for e-NLMS
mse_nlms = np.real(errors_nlms * np.conj(errors_nlms))
mse_nlms_db = 10 * np.log10(mse_nlms + 1e-12)

# Convert EMSE to dB
emse_nlms_db = 10 * np.log10(emse_nlms + 1e-12)

print("Calling C++ GA-LMS Complex binary...")

# Call the Complex GA-LMS binary with parameters
arguments_complex = " {} {} {} {} {}".format(M, L, N, mu_ga_complex, sigma2v)
binary_path_complex = "./{}".format(BINARY_COMPLEX)
cmd_complex = binary_path_complex + arguments_complex
print("Executing: {}".format(cmd_complex))
os.system(cmd_complex)

print("Loading GA-LMS Complex results...")

# Load results from Complex GA-LMS output files
try:
    mse_galms_complex = np.loadtxt('MSE_new_filter.out')
    emse_galms_complex = np.loadtxt('EMSE_new_filter.out')
    x_estimated_galms_complex = load_signal_from_file('x_estimated.out')
    x_input_check_complex = load_signal_from_file('x_input.out')

    # Convert MSE and EMSE to dB
    mse_galms_complex_db = 10 * np.log10(mse_galms_complex + 1e-12)
    emse_galms_complex_db = 10 * np.log10(emse_galms_complex + 1e-12)

except Exception as e:
    print("Error loading Complex GA-LMS results files: {}".format(e))
    mse_galms_complex_db = np.zeros(N)
    emse_galms_complex = np.zeros(N)
    emse_galms_complex_db = np.zeros(N)
    x_estimated_galms_complex = avg_x_noisy  # fallback
    x_input_check_complex = avg_x_noisy

print("Calling C++ GA-LMS Rotors binary...")

# Call the Quaternion Rotors GA-LMS binary with parameters
arguments_rotors = " {} {} {} {} {}".format(M, L, N, mu_ga_rotors, sigma2v)
binary_path_rotors = "./{}".format(BINARY_ROTORS)
cmd_rotors = binary_path_rotors + arguments_rotors
print("Executing: {}".format(cmd_rotors))
os.system(cmd_rotors)

print("Loading GA-LMS Rotors results...")

# Load results from Quaternion Rotors GA-LMS output files
try:
    mse_galms_rotors = np.loadtxt('MSE_new_filter_rotors.out')
    emse_galms_rotors = np.loadtxt('EMSE_new_filter_rotors.out')
    x_estimated_galms_rotors = load_signal_from_file('x_estimated_rotors.out')
    x_input_check_rotors = load_signal_from_file('x_input_rotors.out')

    # Convert MSE and EMSE to dB
    mse_galms_rotors_db = 10 * np.log10(mse_galms_rotors + 1e-12)
    emse_galms_rotors_db = 10 * np.log10(emse_galms_rotors + 1e-12)

except Exception as e:
    print("Error loading Rotors GA-LMS results files: {}".format(e))
    mse_galms_rotors_db = np.zeros(N)
    emse_galms_rotors = np.zeros(N)
    emse_galms_rotors_db = np.zeros(N)
    x_estimated_galms_rotors = avg_x_noisy  # fallback
    x_input_check_rotors = avg_x_noisy

# For backward compatibility, use complex version as primary
mse_galms_db = mse_galms_complex_db
emse_galms_db = emse_galms_complex_db
x_estimated_galms = x_estimated_galms_complex

print("Generating comparison charts...")

# Time vector for plotting
time_vec = np.arange(N)

# ============================================================================
# CHART 1: SIGNAL TRACKING COMPARISON WITH EMSE ANALYSIS
# ============================================================================
plt.figure(figsize=(18, 15))

# Real part comparison
plt.subplot(4, 2, 1)
plt.plot(time_vec[:1000], avg_x_clean[:1000].real, 'b-', linewidth=4, label='True signal (real)')
plt.plot(time_vec[:1000], x_estimated_nlms[:1000].real, 'g--', linewidth=1.5, label='e-NLMS estimate (real)')
if len(x_estimated_galms_complex) > 0:
    plt.plot(time_vec[:1000], x_estimated_galms_complex[:1000].real, 'r--', linewidth=2, label='GA-LMS Complex (real)')
if len(x_estimated_galms_rotors) > 0:
    plt.plot(time_vec[:1000], x_estimated_galms_rotors[:1000].real, 'm--', linewidth=2, label='GA-LMS Rotors (real)')
plt.xlabel('Sample Index')
plt.ylabel('Real Part')
plt.title('Signal Tracking Comparison - Real Part (First 1000 samples)')
plt.legend()
plt.grid(True, alpha=0.3)

# Imaginary part comparison
plt.subplot(4, 2, 2)
plt.plot(time_vec[:1000], avg_x_clean[:1000].imag, 'b-', linewidth=4, label='True signal (imag)')
plt.plot(time_vec[:1000], x_estimated_nlms[:1000].imag, 'g--', linewidth=1.5, label='e-NLMS estimate (imag)')
if len(x_estimated_galms_complex) > 0:
    plt.plot(time_vec[:1000], x_estimated_galms_complex[:1000].imag, 'r--', linewidth=2, label='GA-LMS Complex (imag)')
if len(x_estimated_galms_rotors) > 0:
    plt.plot(time_vec[:1000], x_estimated_galms_rotors[:1000].imag, 'm--', linewidth=2, label='GA-LMS Rotors (imag)')
plt.xlabel('Sample Index')
plt.ylabel('Imaginary Part')
plt.title('Signal Tracking Comparison - Imaginary Part (First 1000 samples)')
plt.legend()
plt.grid(True, alpha=0.3)

# Magnitude comparison
plt.subplot(4, 2, 3)
plt.plot(time_vec[:1000], np.abs(avg_x_clean[:1000]), 'b-', linewidth=2, label='True magnitude')
plt.plot(time_vec[:1000], np.abs(x_estimated_nlms[:1000]), 'g--', linewidth=1.5, label='e-NLMS magnitude')
if len(x_estimated_galms_complex) > 0:
    plt.plot(time_vec[:1000], np.abs(x_estimated_galms_complex[:1000]), 'r--', linewidth=1.5, label='GA-LMS Complex magnitude')
if len(x_estimated_galms_rotors) > 0:
    plt.plot(time_vec[:1000], np.abs(x_estimated_galms_rotors[:1000]), 'm--', linewidth=1.5, label='GA-LMS Rotors magnitude')
plt.plot(time_vec[:1000], np.abs(avg_x_noisy[:1000]), 'k:', linewidth=0.5, alpha=0.7, label='Noisy magnitude')
plt.xlabel('Sample Index')
plt.ylabel('Magnitude')
plt.title('Signal Tracking Comparison - Magnitude')
plt.legend()
plt.grid(True, alpha=0.3)

# Phase comparison
plt.subplot(4, 2, 4)
plt.plot(time_vec[:1000], np.angle(avg_x_clean[:1000]), 'b-', linewidth=2, label='True phase')
plt.plot(time_vec[:1000], np.angle(x_estimated_nlms[:1000]), 'g--', linewidth=1.5, label='e-NLMS phase')
if len(x_estimated_galms_complex) > 0:
    plt.plot(time_vec[:1000], np.angle(x_estimated_galms_complex[:1000]), 'r--', linewidth=1.5, label='GA-LMS Complex phase')
if len(x_estimated_galms_rotors) > 0:
    plt.plot(time_vec[:1000], np.angle(x_estimated_galms_rotors[:1000]), 'm--', linewidth=1.5, label='GA-LMS Rotors phase')
plt.xlabel('Sample Index')
plt.ylabel('Phase (rad)')
plt.title('Signal Tracking Comparison - Phase')
plt.legend()
plt.grid(True, alpha=0.3)

# MSE Learning Curves
plt.subplot(4, 2, 5)
plt.plot(time_vec, mse_nlms_db, 'g-', linewidth=2, label='e-NLMS MSE')
plt.plot(time_vec, mse_galms_complex_db, 'r-', linewidth=2, label='GA-LMS Complex MSE')
plt.plot(time_vec, mse_galms_rotors_db, 'm-', linewidth=2, label='GA-LMS Rotors MSE')
plt.axvline(x=acceleration_peak_time, color='orange', linestyle=':', alpha=0.7, label='Acceleration peak')
plt.axvline(x=parachute_time, color='purple', linestyle=':', alpha=0.7, label='Parachute deployment')
plt.xlabel('Sample Index')
plt.ylabel('MSE (dB)')
plt.title('Learning Curves Comparison')
plt.legend()
plt.grid(True, alpha=0.3)

# EMSE Learning Curves (NEW!)
plt.subplot(4, 2, 6)
plt.plot(time_vec, emse_nlms_db, 'g-', linewidth=2, label='e-NLMS EMSE')
plt.plot(time_vec, emse_galms_complex_db, 'r-', linewidth=2, label='GA-LMS Complex EMSE')
plt.plot(time_vec, emse_galms_rotors_db, 'm-', linewidth=2, label='GA-LMS Rotors EMSE')
plt.axvline(x=acceleration_peak_time, color='orange', linestyle=':', alpha=0.7, label='Acceleration peak')
plt.axvline(x=parachute_time, color='purple', linestyle=':', alpha=0.7, label='Parachute deployment')
plt.xlabel('Sample Index')
plt.ylabel('EMSE (dB)')
plt.title('Excess Mean Square Error Comparison')
plt.legend()
plt.grid(True, alpha=0.3)

# Error magnitude comparison
plt.subplot(4, 2, 7)
error_nlms_mag = np.abs(avg_x_clean - x_estimated_nlms)
plt.plot(time_vec[:1000], error_nlms_mag[:1000], 'g-', linewidth=1.5, label='e-NLMS error magnitude')

if len(x_estimated_galms_complex) > 0:
    error_galms_complex_mag = np.abs(avg_x_clean - x_estimated_galms_complex)
    plt.plot(time_vec[:1000], error_galms_complex_mag[:1000], 'r-', linewidth=1.5, label='GA-LMS Complex error magnitude')

if len(x_estimated_galms_rotors) > 0:
    error_galms_rotors_mag = np.abs(avg_x_clean - x_estimated_galms_rotors)
    plt.plot(time_vec[:1000], error_galms_rotors_mag[:1000], 'm-', linewidth=1.5, label='GA-LMS Rotors error magnitude')

plt.xlabel('Sample Index')
plt.ylabel('Error Magnitude')
plt.title('Tracking Error Magnitude Comparison')
plt.legend()
plt.grid(True, alpha=0.3)

# Noise vs EMSE decomposition analysis
plt.subplot(4, 2, 8)
# Calculate noise component (MSE - EMSE)
noise_component_nlms = mse_nlms - emse_nlms
noise_component_galms_complex = np.zeros_like(emse_nlms)
noise_component_galms_rotors = np.zeros_like(emse_nlms)

if len(x_estimated_galms_complex) > 0:
    noise_component_galms_complex = mse_galms_complex[:len(emse_galms_complex)] - emse_galms_complex

if len(x_estimated_galms_rotors) > 0:
    noise_component_galms_rotors = mse_galms_rotors[:len(emse_galms_rotors)] - emse_galms_rotors

plt.plot(time_vec[:1000], 10*np.log10(noise_component_nlms[:1000] + 1e-12), 'g:', linewidth=1.5, label='e-NLMS Noise Component')
plt.plot(time_vec[:1000], emse_nlms_db[:1000], 'g-', linewidth=2, label='e-NLMS EMSE')
if len(x_estimated_galms_complex) > 0:
    plt.plot(time_vec[:1000], 10*np.log10(noise_component_galms_complex[:1000] + 1e-12), 'r:', linewidth=1.5, label='GA-LMS Complex Noise')
    plt.plot(time_vec[:1000], emse_galms_complex_db[:1000], 'r-', linewidth=2, label='GA-LMS Complex EMSE')
if len(x_estimated_galms_rotors) > 0:
    plt.plot(time_vec[:1000], 10*np.log10(noise_component_galms_rotors[:1000] + 1e-12), 'm:', linewidth=1.5, label='GA-LMS Rotors Noise')
    plt.plot(time_vec[:1000], emse_galms_rotors_db[:1000], 'm-', linewidth=2, label='GA-LMS Rotors EMSE')
plt.xlabel('Sample Index')
plt.ylabel('Power (dB)')
plt.title('Error Decomposition: EMSE vs Noise')
plt.legend()
plt.grid(True, alpha=0.3)

plt.suptitle('Mars EDL Signal Tracking: e-NLMS vs GA-LMS Complex vs GA-LMS Rotors', fontsize=16, fontweight='bold')
plt.tight_layout()
pp.savefig()
plt.close()

# ============================================================================
# CHART 2: DETAILED PERFORMANCE ANALYSIS
# ============================================================================
plt.figure(figsize=(15, 10))

# Full signal real part tracking
plt.subplot(2, 2, 1)
plt.plot(time_vec, avg_x_clean.real, 'b-', linewidth=3, label='True signal (real)', alpha=0.8)
plt.plot(time_vec, x_estimated_nlms.real, 'g-', linewidth=1, label='e-NLMS estimate (real)')
if len(x_estimated_galms_complex) > 0:
    plt.plot(time_vec, x_estimated_galms_complex.real, 'r-', linewidth=1, label='GA-LMS Complex estimate (real)')
if len(x_estimated_galms_rotors) > 0:
    plt.plot(time_vec, x_estimated_galms_rotors.real, 'm-', linewidth=1, label='GA-LMS Rotors estimate (real)')
plt.axvline(x=acceleration_peak_time, color='orange', linestyle=':', linewidth=2, alpha=0.9)
plt.axvline(x=parachute_time, color='purple', linestyle=':', linewidth=2, alpha=0.9)
plt.xlabel('Sample Index')
plt.ylabel('Real Part')
plt.title('Complete Signal Tracking - Real Part')
plt.legend()
plt.grid(True, alpha=0.3)

# Full signal imaginary part tracking
plt.subplot(2, 2, 2)
plt.plot(time_vec, avg_x_clean.imag, 'b-', linewidth=3, label='True signal (imag)', alpha=0.8)
plt.plot(time_vec, x_estimated_nlms.imag, 'g-', linewidth=1, label='e-NLMS estimate (imag)')
if len(x_estimated_galms_complex) > 0:
    plt.plot(time_vec, x_estimated_galms_complex.imag, 'r-', linewidth=1, label='GA-LMS Complex estimate (imag)')
if len(x_estimated_galms_rotors) > 0:
    plt.plot(time_vec, x_estimated_galms_rotors.imag, 'm-', linewidth=1, label='GA-LMS Rotors estimate (imag)')
plt.axvline(x=acceleration_peak_time, color='orange', linestyle=':', linewidth=2, alpha=0.9)
plt.axvline(x=parachute_time, color='purple', linestyle=':', linewidth=2, alpha=0.9)
plt.xlabel('Sample Index')
plt.ylabel('Imaginary Part')
plt.title('Complete Signal Tracking - Imaginary Part')
plt.legend()
plt.grid(True, alpha=0.3)

# MSE comparison during critical periods
plt.subplot(2, 2, 3)
critical_start = max(0, acceleration_peak_time - 200)
critical_end = min(len(mse_nlms_db), parachute_time + 300)
critical_range = slice(critical_start, critical_end)
critical_time = time_vec[critical_range]

plt.plot(critical_time, mse_nlms_db[critical_range], 'g-', linewidth=2, label='e-NLMS MSE')
if len(mse_galms_complex_db) > 0:
    plt.plot(critical_time, mse_galms_complex_db[critical_range], 'r-', linewidth=2, label='GA-LMS Complex MSE')
if len(mse_galms_rotors_db) > 0:
    plt.plot(critical_time, mse_galms_rotors_db[critical_range], 'm-', linewidth=2, label='GA-LMS Rotors MSE')
plt.axvline(x=acceleration_peak_time, color='orange', linestyle=':', alpha=0.7, label='Acceleration peak')
plt.axvline(x=parachute_time, color='purple', linestyle=':', alpha=0.7, label='Parachute deployment')
plt.xlabel('Sample Index')
plt.ylabel('MSE (dB)')
plt.title('MSE During Critical EDL Periods')
plt.legend()
plt.grid(True, alpha=0.3)

# Cumulative performance comparison
plt.subplot(2, 2, 4)
cumulative_mse_nlms = np.cumsum(mse_nlms_db) / np.arange(1, len(mse_nlms_db) + 1)
if len(mse_galms_complex_db) > 0:
    cumulative_mse_galms_complex = np.cumsum(mse_galms_complex_db) / np.arange(1, len(mse_galms_complex_db) + 1)
if len(mse_galms_rotors_db) > 0:
    cumulative_mse_galms_rotors = np.cumsum(mse_galms_rotors_db) / np.arange(1, len(mse_galms_rotors_db) + 1)

plt.plot(time_vec, cumulative_mse_nlms, 'g-', linewidth=2, label='e-NLMS Cumulative MSE')
if len(mse_galms_complex_db) > 0:
    plt.plot(time_vec, cumulative_mse_galms_complex, 'r-', linewidth=2, label='GA-LMS Complex Cumulative MSE')
if len(mse_galms_rotors_db) > 0:
    plt.plot(time_vec, cumulative_mse_galms_rotors, 'm-', linewidth=2, label='GA-LMS Rotors Cumulative MSE')
plt.axvline(x=acceleration_peak_time, color='orange', linestyle=':', alpha=0.5)
plt.axvline(x=parachute_time, color='purple', linestyle=':', alpha=0.5)
plt.xlabel('Sample Index')
plt.ylabel('Cumulative Average MSE (dB)')
plt.title('Cumulative Performance Comparison')
plt.legend()
plt.grid(True, alpha=0.3)

plt.suptitle('Detailed Performance Analysis: GA-LMS vs e-NLMS', fontsize=16, fontweight='bold')
plt.tight_layout()
pp.savefig()
plt.close()

# Print summary statistics
print("\n" + "="*80)
print("MARS EDL SIGNAL TRACKING COMPARISON: e-NLMS vs GA-LMS Complex vs GA-LMS Rotors")
print("="*80)
print("Parameters:")
print("  System order (M): {}".format(M))
print("  Realizations (L): {}".format(L))
print("  Iterations (N): {}".format(N))
print("  e-NLMS Step size (mu): {}".format(mu))
print("  GA-LMS Complex Step size (mu_ga_complex): {}".format(mu_ga_complex))
print("  GA-LMS Rotors Step size (mu_ga_rotors): {}".format(mu_ga_rotors))
print("  Noise variance (sigma2v): {}".format(sigma2v))
print("  Sampling frequency: {} Hz".format(Fs))

print("\nMars EDL Timeline:")
print("  Acceleration peak: sample {}".format(acceleration_peak_time))
print("  Parachute deployment: sample {}".format(parachute_time))

print("\nPerformance Comparison:")
final_mse_nlms = mse_nlms_db[-100:].mean() if len(mse_nlms_db) > 100 else mse_nlms_db[-1]
final_mse_galms_complex = mse_galms_complex_db[-100:].mean() if len(mse_galms_complex_db) > 100 else mse_galms_complex_db[-1]
final_mse_galms_rotors = mse_galms_rotors_db[-100:].mean() if len(mse_galms_rotors_db) > 100 else mse_galms_rotors_db[-1]
print("  e-NLMS Final MSE: {:.2f} dB".format(final_mse_nlms))
print("  GA-LMS Complex Final MSE: {:.2f} dB".format(final_mse_galms_complex))
print("  GA-LMS Rotors Final MSE: {:.2f} dB".format(final_mse_galms_rotors))

# EMSE Performance Analysis
final_emse_nlms = emse_nlms_db[-100:].mean() if len(emse_nlms_db) > 100 else emse_nlms_db[-1]
final_emse_galms_complex = emse_galms_complex_db[-100:].mean() if len(emse_galms_complex_db) > 100 else emse_galms_complex_db[-1]
final_emse_galms_rotors = emse_galms_rotors_db[-100:].mean() if len(emse_galms_rotors_db) > 100 else emse_galms_rotors_db[-1]
print("\nExcess Mean Square Error (EMSE) Analysis:")
print("  e-NLMS Final EMSE: {:.2f} dB".format(final_emse_nlms))
print("  GA-LMS Complex Final EMSE: {:.2f} dB".format(final_emse_galms_complex))
print("  GA-LMS Rotors Final EMSE: {:.2f} dB".format(final_emse_galms_rotors))

# Calculate noise floor (difference between MSE and EMSE)
noise_floor_nlms = final_mse_nlms - final_emse_nlms
noise_floor_galms_complex = final_mse_galms_complex - final_emse_galms_complex
noise_floor_galms_rotors = final_mse_galms_rotors - final_emse_galms_rotors
print("  e-NLMS Noise Floor: {:.2f} dB".format(noise_floor_nlms))
print("  GA-LMS Complex Noise Floor: {:.2f} dB".format(noise_floor_galms_complex))
print("  GA-LMS Rotors Noise Floor: {:.2f} dB".format(noise_floor_galms_rotors))

# MSE Comparison - Complex vs e-NLMS
print("\nMSE Performance Analysis:")
if final_mse_galms_complex < final_mse_nlms:
    improvement_complex = final_mse_nlms - final_mse_galms_complex
    print("  GA-LMS Complex vs e-NLMS: {:.2f} dB improvement".format(improvement_complex))
else:
    degradation_complex = final_mse_galms_complex - final_mse_nlms
    print("  GA-LMS Complex vs e-NLMS: {:.2f} dB worse".format(degradation_complex))

# MSE Comparison - Rotors vs e-NLMS
if final_mse_galms_rotors < final_mse_nlms:
    improvement_rotors = final_mse_nlms - final_mse_galms_rotors
    print("  GA-LMS Rotors vs e-NLMS: {:.2f} dB improvement".format(improvement_rotors))
else:
    degradation_rotors = final_mse_galms_rotors - final_mse_nlms
    print("  GA-LMS Rotors vs e-NLMS: {:.2f} dB worse".format(degradation_rotors))

# MSE Comparison - Complex vs Rotors
if final_mse_galms_complex < final_mse_galms_rotors:
    complex_advantage = final_mse_galms_rotors - final_mse_galms_complex
    print("  GA-LMS Complex vs Rotors: {:.2f} dB better".format(complex_advantage))
else:
    rotors_advantage = final_mse_galms_complex - final_mse_galms_rotors
    print("  GA-LMS Rotors vs Complex: {:.2f} dB better".format(rotors_advantage))

# EMSE Comparison - Complex vs e-NLMS
print("\nEMSE Performance Analysis:")
if final_emse_galms_complex < final_emse_nlms:
    emse_improvement_complex = final_emse_nlms - final_emse_galms_complex
    print("  GA-LMS Complex vs e-NLMS: {:.2f} dB improvement".format(emse_improvement_complex))
else:
    emse_degradation_complex = final_emse_galms_complex - final_emse_nlms
    print("  GA-LMS Complex vs e-NLMS: {:.2f} dB worse".format(emse_degradation_complex))

# EMSE Comparison - Rotors vs e-NLMS
if final_emse_galms_rotors < final_emse_nlms:
    emse_improvement_rotors = final_emse_nlms - final_emse_galms_rotors
    print("  GA-LMS Rotors vs e-NLMS: {:.2f} dB improvement".format(emse_improvement_rotors))
else:
    emse_degradation_rotors = final_emse_galms_rotors - final_emse_nlms
    print("  GA-LMS Rotors vs e-NLMS: {:.2f} dB worse".format(emse_degradation_rotors))

# EMSE Comparison - Complex vs Rotors
if final_emse_galms_complex < final_emse_galms_rotors:
    emse_complex_advantage = final_emse_galms_rotors - final_emse_galms_complex
    print("  GA-LMS Complex vs Rotors: {:.2f} dB better".format(emse_complex_advantage))
else:
    emse_rotors_advantage = final_emse_galms_complex - final_emse_galms_rotors
    print("  GA-LMS Rotors vs Complex: {:.2f} dB better".format(emse_rotors_advantage))

# Convergence analysis
print("\nConvergence Analysis:")
steady_state_start = max(7500, N - 1000)  # After final discontinuity (sample 7000)
emse_nlms_steady = emse_nlms_db[steady_state_start:].mean()
emse_galms_complex_steady = emse_galms_complex_db[steady_state_start:].mean()
emse_galms_rotors_steady = emse_galms_rotors_db[steady_state_start:].mean()
print("  e-NLMS Steady-state EMSE: {:.2f} dB".format(emse_nlms_steady))
print("  GA-LMS Complex Steady-state EMSE: {:.2f} dB".format(emse_galms_complex_steady))
print("  GA-LMS Rotors Steady-state EMSE: {:.2f} dB".format(emse_galms_rotors_steady))

# Signal tracking quality assessment
print("\nSignal Tracking Quality:")

# e-NLMS tracking errors
real_error_nlms = np.mean(np.abs(avg_x_clean.real - x_estimated_nlms.real))
imag_error_nlms = np.mean(np.abs(avg_x_clean.imag - x_estimated_nlms.imag))
complex_error_nlms = np.mean(np.abs(avg_x_clean - x_estimated_nlms))

print("  e-NLMS Real part MAE: {:.6f}".format(real_error_nlms))
print("  e-NLMS Imag part MAE: {:.6f}".format(imag_error_nlms))
print("  e-NLMS Complex signal MAE: {:.6f}".format(complex_error_nlms))

# GA-LMS Complex tracking errors
if len(x_estimated_galms_complex) > 0:
    real_error_galms_complex = np.mean(np.abs(avg_x_clean.real - x_estimated_galms_complex.real))
    imag_error_galms_complex = np.mean(np.abs(avg_x_clean.imag - x_estimated_galms_complex.imag))
    complex_error_galms_complex = np.mean(np.abs(avg_x_clean - x_estimated_galms_complex))

    print("  GA-LMS Complex Real part MAE: {:.6f}".format(real_error_galms_complex))
    print("  GA-LMS Complex Imag part MAE: {:.6f}".format(imag_error_galms_complex))
    print("  GA-LMS Complex signal MAE: {:.6f}".format(complex_error_galms_complex))

# GA-LMS Rotors tracking errors
if len(x_estimated_galms_rotors) > 0:
    real_error_galms_rotors = np.mean(np.abs(avg_x_clean.real - x_estimated_galms_rotors.real))
    imag_error_galms_rotors = np.mean(np.abs(avg_x_clean.imag - x_estimated_galms_rotors.imag))
    complex_error_galms_rotors = np.mean(np.abs(avg_x_clean - x_estimated_galms_rotors))

    print("  GA-LMS Rotors Real part MAE: {:.6f}".format(real_error_galms_rotors))
    print("  GA-LMS Rotors Imag part MAE: {:.6f}".format(imag_error_galms_rotors))
    print("  GA-LMS Rotors Complex signal MAE: {:.6f}".format(complex_error_galms_rotors))

# Critical periods analysis
accel_indices = slice(max(0, acceleration_peak_time-100), min(N, acceleration_peak_time+100))
parachute_indices = slice(max(0, parachute_time-100), min(N, parachute_time+100))

accel_error_nlms = np.mean(np.abs(avg_x_clean[accel_indices] - x_estimated_nlms[accel_indices]))
parachute_error_nlms = np.mean(np.abs(avg_x_clean[parachute_indices] - x_estimated_nlms[parachute_indices]))

print("\nCritical EDL Period Analysis:")
print("  Acceleration peak period:")
print("    e-NLMS MAE: {:.6f}".format(accel_error_nlms))

if len(x_estimated_galms_complex) > 0:
    accel_error_galms_complex = np.mean(np.abs(avg_x_clean[accel_indices] - x_estimated_galms_complex[accel_indices]))
    parachute_error_galms_complex = np.mean(np.abs(avg_x_clean[parachute_indices] - x_estimated_galms_complex[parachute_indices]))
    print("    GA-LMS Complex MAE: {:.6f}".format(accel_error_galms_complex))

if len(x_estimated_galms_rotors) > 0:
    accel_error_galms_rotors = np.mean(np.abs(avg_x_clean[accel_indices] - x_estimated_galms_rotors[accel_indices]))
    parachute_error_galms_rotors = np.mean(np.abs(avg_x_clean[parachute_indices] - x_estimated_galms_rotors[parachute_indices]))
    print("    GA-LMS Rotors MAE: {:.6f}".format(accel_error_galms_rotors))

print("  Parachute deployment period:")
print("    e-NLMS MAE: {:.6f}".format(parachute_error_nlms))

if len(x_estimated_galms_complex) > 0:
    print("    GA-LMS Complex MAE: {:.6f}".format(parachute_error_galms_complex))

if len(x_estimated_galms_rotors) > 0:
    print("    GA-LMS Rotors MAE: {:.6f}".format(parachute_error_galms_rotors))

print("="*80)

pp.close()
print("\nResults saved to: mars_edl_signal_tracking_comparison.pdf")
print("Mars EDL Signal Tracking Comparison completed successfully!")
