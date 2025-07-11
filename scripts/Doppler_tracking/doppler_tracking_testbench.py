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
L       = 10    # Realizations
N       = 3500  # Time iterations (matching the paper's time scale)
mu      = 1e-3  # AF Step size
sigma2v = 1e-2  # Variance of measurement noise
Fs      = 100   # Sampling frequency (Hz)

# Mars EDL Doppler profile parameters (from the paper figure)
f0 = 0          # Nominal frequency (after down-conversion)
acceleration_peak_time = 1000   # Time of acceleration peak (sample index)
parachute_time = 2500          # Time of parachute deployment (sample index)

BINARY = '../../src/GAAFs_doppler/doppler_galms/build/doppler_galms'  # Your modified C++ binary name
#====================================================

def generate_mars_edl_doppler_profile(N):
    """
    Generate the exact Doppler frequency profile from the Mars EDL communications paper
    This matches Figure 2 from the paper showing the typical EDL Doppler profile
    """
    # Time vector (sample indices)
    t = np.arange(N)
    
    # Initialize frequency profile
    f_doppler = np.zeros(N)
    
    # Phase 1: Initial descent (samples 0 to ~500) - gradual decrease from ~-30 Hz to ~-35 Hz
    phase1_end = 500
    phase1_mask = t < phase1_end
    f_doppler[phase1_mask] = -30 - 5 * (t[phase1_mask] / phase1_end)
    
    # Phase 2: Acceleration build-up (samples 500 to 1000) - sharp increase from -35 Hz to +25 Hz
    phase2_start = 500
    phase2_end = acceleration_peak_time
    phase2_mask = (t >= phase2_start) & (t < phase2_end)
    # Quadratic increase to simulate acceleration
    phase2_progress = (t[phase2_mask] - phase2_start) / (phase2_end - phase2_start)
    f_doppler[phase2_mask] = -35 + 60 * (phase2_progress ** 2)
    
    # Phase 3: Peak acceleration (samples 1000 to 1500) - maintain around +25 Hz with slight variations
    phase3_start = acceleration_peak_time
    phase3_end = 1500
    phase3_mask = (t >= phase3_start) & (t < phase3_end)
    # Add some realistic variations during peak acceleration
    phase3_progress = (t[phase3_mask] - phase3_start) / (phase3_end - phase3_start)
    f_doppler[phase3_mask] = 25 + 5 * np.sin(4 * pi * phase3_progress) * np.exp(-2 * phase3_progress)
    
    # Phase 4: Pre-parachute dynamics (samples 1500 to 2500) - complex dynamics leading to parachute deployment
    phase4_start = 1500
    phase4_end = parachute_time
    phase4_mask = (t >= phase4_start) & (t < phase4_end)
    phase4_progress = (t[phase4_mask] - phase4_start) / (phase4_end - phase4_start)
    # Oscillatory behavior before parachute deployment
    f_doppler[phase4_mask] = 25 * (1 - 0.6 * phase4_progress) + 10 * np.sin(6 * pi * phase4_progress) * (1 - phase4_progress)
    
    # Phase 5: Parachute deployment (samples 2500 to 2800) - rapid change due to parachute
    phase5_start = parachute_time
    phase5_end = 2800
    phase5_mask = (t >= phase5_start) & (t < phase5_end)
    phase5_progress = (t[phase5_mask] - phase5_start) / (phase5_end - phase5_start)
    # Sharp transition during parachute deployment
    f_doppler[phase5_mask] = 10 * (1 - phase5_progress) - 20 * phase5_progress
    
    # Phase 6: Post-parachute descent (samples 2800 to end) - gradual approach to landing
    phase6_start = 2800
    phase6_mask = t >= phase6_start
    phase6_progress = (t[phase6_mask] - phase6_start) / (N - phase6_start)
    # Exponential decay to final approach
    f_doppler[phase6_mask] = -20 * np.exp(-2 * phase6_progress) + 5 * np.sin(2 * pi * phase6_progress) * np.exp(-3 * phase6_progress)
    
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
    
    def __init__(self, M, mu, epsilon=1e-4):
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

# Process signal with e-NLMS
epsilon_nlms = EpsilonNLMS(M=M, mu=mu, epsilon=1e-4)
x_estimated_nlms, errors_nlms = epsilon_nlms.process_signal(avg_x_noisy)

# Calculate MSE for e-NLMS
mse_nlms = np.real(errors_nlms * np.conj(errors_nlms))
mse_nlms_db = 10 * np.log10(mse_nlms + 1e-12)

print("Calling C++ GA-LMS binary...")

# Call the C++ binary with parameters
arguments = " {} {} {} {} {}".format(M, L, N, mu, sigma2v)
binary_path = "./{}".format(BINARY)
cmd = binary_path + arguments
print("Executing: {}".format(cmd))
os.system(cmd)

print("Loading GA-LMS results...")

# Load results from C++ output files
try:
    mse_galms = np.loadtxt('MSE_new_filter.out')
    
    # Load estimated signal
    x_estimated_galms = load_signal_from_file('x_estimated.out')
    x_input_check = load_signal_from_file('x_input.out')
    
    # Convert MSE to dB
    mse_galms_db = 10 * np.log10(mse_galms + 1e-12)
    
except Exception as e:
    print("Error loading results files: {}".format(e))
    mse_galms_db = np.zeros(N)
    x_estimated_galms = avg_x_noisy  # fallback
    x_input_check = avg_x_noisy

print("Generating comparison charts...")

# Time vector for plotting
time_vec = np.arange(N)

# ============================================================================
# CHART 1: SIGNAL TRACKING COMPARISON - REAL PART
# ============================================================================
plt.figure(figsize=(15, 12))

# Real part comparison
plt.subplot(3, 2, 1)
plt.plot(time_vec[:1000], avg_x_clean[:1000].real, 'b-', linewidth=4, label='True signal (real)')
plt.plot(time_vec[:1000], x_estimated_nlms[:1000].real, 'g--', linewidth=1.5, label='e-NLMS estimate (real)')
if len(x_estimated_galms) > 0:
    plt.plot(time_vec[:1000], x_estimated_galms[:1000].real, 'r--', linewidth=2, label='GA-LMS estimate (real)')
#plt.plot(time_vec[:1000], avg_x_noisy[:1000].real, 'k:', linewidth=0.5, alpha=0.7, label='Noisy input (real)')
plt.xlabel('Sample Index')
plt.ylabel('Real Part')
plt.title('Signal Tracking Comparison - Real Part (First 1000 samples)')
plt.legend()
plt.grid(True, alpha=0.3)

# Imaginary part comparison
plt.subplot(3, 2, 2)
plt.plot(time_vec[:1000], avg_x_clean[:1000].imag, 'b-', linewidth=4, label='True signal (imag)')
plt.plot(time_vec[:1000], x_estimated_nlms[:1000].imag, 'g--', linewidth=1.5, label='e-NLMS estimate (imag)')
if len(x_estimated_galms) > 0:
    plt.plot(time_vec[:1000], x_estimated_galms[:1000].imag, 'r--', linewidth=2, label='GA-LMS estimate (imag)')
#plt.plot(time_vec[:1000], avg_x_noisy[:1000].imag, 'k:', linewidth=0.5, alpha=0.7, label='Noisy input (imag)')
plt.xlabel('Sample Index')
plt.ylabel('Imaginary Part')
plt.title('Signal Tracking Comparison - Imaginary Part (First 1000 samples)')
plt.legend()
plt.grid(True, alpha=0.3)

# Magnitude comparison
plt.subplot(3, 2, 3)
plt.plot(time_vec[:1000], np.abs(avg_x_clean[:1000]), 'b-', linewidth=2, label='True magnitude')
plt.plot(time_vec[:1000], np.abs(x_estimated_nlms[:1000]), 'g--', linewidth=1.5, label='e-NLMS magnitude')
if len(x_estimated_galms) > 0:
    plt.plot(time_vec[:1000], np.abs(x_estimated_galms[:1000]), 'r--', linewidth=1.5, label='GA-LMS magnitude')
plt.plot(time_vec[:1000], np.abs(avg_x_noisy[:1000]), 'k:', linewidth=0.5, alpha=0.7, label='Noisy magnitude')
plt.xlabel('Sample Index')
plt.ylabel('Magnitude')
plt.title('Signal Tracking Comparison - Magnitude')
plt.legend()
plt.grid(True, alpha=0.3)

# Phase comparison
plt.subplot(3, 2, 4)
plt.plot(time_vec[:1000], np.angle(avg_x_clean[:1000]), 'b-', linewidth=2, label='True phase')
plt.plot(time_vec[:1000], np.angle(x_estimated_nlms[:1000]), 'g--', linewidth=1.5, label='e-NLMS phase')
if len(x_estimated_galms) > 0:
    plt.plot(time_vec[:1000], np.angle(x_estimated_galms[:1000]), 'r--', linewidth=1.5, label='GA-LMS phase')
plt.xlabel('Sample Index')
plt.ylabel('Phase (rad)')
plt.title('Signal Tracking Comparison - Phase')
plt.legend()
plt.grid(True, alpha=0.3)

# MSE Learning Curves
plt.subplot(3, 2, 5)
plt.plot(time_vec, mse_nlms_db, 'g-', linewidth=2, label='e-NLMS MSE')
plt.plot(time_vec, mse_galms_db, 'r-', linewidth=2, label='GA-LMS MSE')
plt.axvline(x=acceleration_peak_time, color='orange', linestyle=':', alpha=0.7, label='Acceleration peak')
plt.axvline(x=parachute_time, color='purple', linestyle=':', alpha=0.7, label='Parachute deployment')
plt.xlabel('Sample Index')
plt.ylabel('MSE (dB)')
plt.title('Learning Curves Comparison')
plt.legend()
plt.grid(True, alpha=0.3)

# Error magnitude comparison
plt.subplot(3, 2, 6)
error_nlms_mag = np.abs(avg_x_clean - x_estimated_nlms)
if len(x_estimated_galms) > 0:
    error_galms_mag = np.abs(avg_x_clean - x_estimated_galms)
    plt.plot(time_vec[:1000], error_galms_mag[:1000], 'r-', linewidth=1.5, label='GA-LMS error magnitude')
plt.plot(time_vec[:1000], error_nlms_mag[:1000], 'g-', linewidth=1.5, label='e-NLMS error magnitude')
plt.xlabel('Sample Index')
plt.ylabel('Error Magnitude')
plt.title('Tracking Error Magnitude Comparison')
plt.legend()
plt.grid(True, alpha=0.3)

plt.suptitle('Mars EDL Signal Tracking: GA-LMS vs e-NLMS Comparison', fontsize=16, fontweight='bold')
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
if len(x_estimated_galms) > 0:
    plt.plot(time_vec, x_estimated_galms.real, 'r-', linewidth=1, label='GA-LMS estimate (real)')
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
if len(x_estimated_galms) > 0:
    plt.plot(time_vec, x_estimated_galms.imag, 'r-', linewidth=1, label='GA-LMS estimate (imag)')
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
plt.plot(critical_time, mse_galms_db[critical_range], 'r-', linewidth=2, label='GA-LMS MSE')
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
cumulative_mse_galms = np.cumsum(mse_galms_db) / np.arange(1, len(mse_galms_db) + 1)

plt.plot(time_vec, cumulative_mse_nlms, 'g-', linewidth=2, label='e-NLMS Cumulative MSE')
plt.plot(time_vec, cumulative_mse_galms, 'r-', linewidth=2, label='GA-LMS Cumulative MSE')
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
print("MARS EDL SIGNAL TRACKING COMPARISON: GA-LMS vs e-NLMS")
print("="*80)
print("Parameters:")
print("  System order (M): {}".format(M))
print("  Realizations (L): {}".format(L))
print("  Iterations (N): {}".format(N))
print("  Step size (mu): {}".format(mu))
print("  Noise variance (sigma2v): {}".format(sigma2v))
print("  Sampling frequency: {} Hz".format(Fs))

print("\nMars EDL Timeline:")
print("  Acceleration peak: sample {}".format(acceleration_peak_time))
print("  Parachute deployment: sample {}".format(parachute_time))

print("\nPerformance Comparison:")
final_mse_nlms = mse_nlms_db[-100:].mean() if len(mse_nlms_db) > 100 else mse_nlms_db[-1]
final_mse_galms = mse_galms_db[-100:].mean() if len(mse_galms_db) > 100 else mse_galms_db[-1]
print("  e-NLMS Final MSE: {:.2f} dB".format(final_mse_nlms))
print("  GA-LMS Final MSE: {:.2f} dB".format(final_mse_galms))

if final_mse_galms < final_mse_nlms:
    improvement = final_mse_nlms - final_mse_galms
    print("  GA-LMS improvement: {:.2f} dB".format(improvement))
    print("  SUCCESS: GA-LMS outperforms e-NLMS!")
else:
    degradation = final_mse_galms - final_mse_nlms
    print("  e-NLMS better by: {:.2f} dB".format(degradation))
    print("  e-NLMS shows better performance")

# Signal tracking quality assessment
if len(x_estimated_galms) > 0:
    # Real part tracking error
    real_error_nlms = np.mean(np.abs(avg_x_clean.real - x_estimated_nlms.real))
    real_error_galms = np.mean(np.abs(avg_x_clean.real - x_estimated_galms.real))
    
    # Imaginary part tracking error
    imag_error_nlms = np.mean(np.abs(avg_x_clean.imag - x_estimated_nlms.imag))
    imag_error_galms = np.mean(np.abs(avg_x_clean.imag - x_estimated_galms.imag))
    
    print("\nSignal Tracking Quality:")
    print("  e-NLMS Real part MAE: {:.6f}".format(real_error_nlms))
    print("  GA-LMS Real part MAE: {:.6f}".format(real_error_galms))
    print("  e-NLMS Imag part MAE: {:.6f}".format(imag_error_nlms))
    print("  GA-LMS Imag part MAE: {:.6f}".format(imag_error_galms))
    
    # Overall complex signal tracking
    complex_error_nlms = np.mean(np.abs(avg_x_clean - x_estimated_nlms))
    complex_error_galms = np.mean(np.abs(avg_x_clean - x_estimated_galms))
    
    print("  e-NLMS Complex signal MAE: {:.6f}".format(complex_error_nlms))
    print("  GA-LMS Complex signal MAE: {:.6f}".format(complex_error_galms))
    
    if complex_error_galms < complex_error_nlms:
        improvement_pct = ((complex_error_nlms - complex_error_galms) / complex_error_nlms) * 100
        print("  GA-LMS shows {:.1f}% better signal tracking".format(improvement_pct))
    else:
        degradation_pct = ((complex_error_galms - complex_error_nlms) / complex_error_nlms) * 100
        print("  e-NLMS shows {:.1f}% better signal tracking".format(degradation_pct))

    # Critical periods analysis
    accel_indices = slice(max(0, acceleration_peak_time-100), min(N, acceleration_peak_time+100))
    parachute_indices = slice(max(0, parachute_time-100), min(N, parachute_time+100))
    
    accel_error_nlms = np.mean(np.abs(avg_x_clean[accel_indices] - x_estimated_nlms[accel_indices]))
    accel_error_galms = np.mean(np.abs(avg_x_clean[accel_indices] - x_estimated_galms[accel_indices]))
    
    parachute_error_nlms = np.mean(np.abs(avg_x_clean[parachute_indices] - x_estimated_nlms[parachute_indices]))
    parachute_error_galms = np.mean(np.abs(avg_x_clean[parachute_indices] - x_estimated_galms[parachute_indices]))
    
    print("\nCritical EDL Period Analysis:")
    print("  Acceleration peak period:")
    print("    e-NLMS MAE: {:.6f}".format(accel_error_nlms))
    print("    GA-LMS MAE: {:.6f}".format(accel_error_galms))
    print("  Parachute deployment period:")
    print("    e-NLMS MAE: {:.6f}".format(parachute_error_nlms))
    print("    GA-LMS MAE: {:.6f}".format(parachute_error_galms))

print("="*80)

pp.close()
print("\nResults saved to: mars_edl_signal_tracking_comparison.pdf")
print("Mars EDL Signal Tracking Comparison completed successfully!")
