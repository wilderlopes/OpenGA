import numpy as np
import matplotlib.pyplot as plt

def generate_doppler_profile(total_samples=3500):
    """
    Generate a realistic noisy Doppler profile for EDL procedures matching actual data
    
    Parameters:
    total_samples: Total number of time samples
    
    Returns:
    time_samples: Array of time indices
    frequency: Array of Doppler frequency values in Hz
    """
    
    time_samples = np.arange(total_samples)
    frequency = np.zeros(total_samples)
    
    # 1. Initial descent: Noisy around -32 Hz (samples 0-800)
    initial_end = 800
    base_freq = -32
    noise_amplitude = 2.5  # Significant noise like in real data
    frequency[:initial_end] = base_freq + np.random.normal(0, noise_amplitude, initial_end)
    
    # 2. Acceleration phase: S-curve from -35 Hz to +10 Hz with noise (samples 800-1300)
    accel_start = 800
    accel_end = 1300
    accel_samples = accel_end - accel_start
    
    # Create sigmoid curve for smooth transition
    x = np.linspace(-4, 4, accel_samples)
    sigmoid = 1 / (1 + np.exp(-x))
    
    # Map sigmoid from [-35, +10] Hz
    start_freq = -35
    end_freq = 10
    base_curve = start_freq + (end_freq - start_freq) * sigmoid
    
    # Add noise during acceleration
    accel_noise = np.random.normal(0, 1.5, accel_samples)
    frequency[accel_start:accel_end] = base_curve + accel_noise
    
    # 3. Acceleration peak: Noisy around +10 Hz (samples 1300-1600)
    peak_start = 1300
    peak_end = 1600
    peak_base = 10
    peak_noise = np.random.normal(0, 3.0, peak_end - peak_start)  # Higher noise during turbulent phase
    frequency[peak_start:peak_end] = peak_base + peak_noise
    
    # 4. Pre-parachute: Gradual noisy increase from +10 Hz to +18 Hz (samples 1600-2400)
    pre_chute_start = 1600
    pre_chute_end = 2400
    pre_chute_samples = pre_chute_end - pre_chute_start
    
    # Base trend line
    base_trend = np.linspace(10, 18, pre_chute_samples)
    
    # Add substantial noise
    pre_chute_noise = np.random.normal(0, 2.0, pre_chute_samples)
    frequency[pre_chute_start:pre_chute_end] = base_trend + pre_chute_noise
    
    # 5. Parachute deployment: Sharp rise with noise (samples 2400-2500)
    deploy_start = 2400
    deploy_end = 2500
    deploy_samples = deploy_end - deploy_start
    
    # Sharp transition from ~18 to ~23 Hz
    deploy_trend = np.linspace(18, 23, deploy_samples)
    deploy_noise = np.random.normal(0, 1.0, deploy_samples)
    frequency[deploy_start:deploy_end] = deploy_trend + deploy_noise
    
    # 6. Post-parachute: Very noisy around +23 Hz (samples 2500-3500)
    post_chute_start = 2500
    stable_freq = 23
    post_samples = total_samples - post_chute_start
    
    # High noise in post-parachute phase (like real data shows)
    post_noise = np.random.normal(0, 1.8, post_samples)
    frequency[post_chute_start:] = stable_freq + post_noise
    
    return time_samples, frequency

def plot_doppler_profile(time_samples, frequency):
    """
    Plot the Doppler profile matching the realistic noisy data
    """
    plt.figure(figsize=(14, 8))
    
    # Main plot - thick black line to match the reference
    plt.plot(time_samples, frequency, 'k-', linewidth=0.8, alpha=0.8)
    
    # Add vertical grid lines
    for x in range(500, 3500, 500):
        plt.axvline(x=x, color='lightgray', linestyle='-', alpha=0.7, linewidth=0.8)
    
    # Add horizontal grid lines
    for y in range(-40, 50, 10):
        plt.axhline(y=y, color='lightgray', linestyle='-', alpha=0.7, linewidth=0.8)
    
    # Labels and title
    plt.xlabel('Time i', fontsize=14, fontweight='bold')
    plt.ylabel('Frequency - Hz', fontsize=14, fontweight='bold')
    
    # Title box at the top
    plt.text(1750, 37, 'Typical Doppler profile\nduring EDL procedures', 
             fontsize=12, fontweight='bold', ha='center', va='center',
             bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="black"))
    
    # Set axis limits to match reference image
    plt.xlim(0, 3500)
    plt.ylim(-40, 40)
    
    # Add annotations with boxes
    # Acceleration peak annotation
    plt.text(1000, 30, 'Acceleration peak', 
             fontsize=10, fontweight='bold', ha='center', va='center',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="black", linestyle='--'))
    
    # Arrow pointing to acceleration peak area
    plt.annotate('', xy=(1200, 15), xytext=(1000, 27),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    
    # Parachute deployment annotation
    plt.text(2700, 5, 'Parachute deployment', 
             fontsize=10, fontweight='bold', ha='center', va='center', color='blue',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="blue", linestyle='--'))
    
    # Arrow pointing to parachute deployment
    plt.annotate('', xy=(2450, 20), xytext=(2650, 8),
                arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))
    
    plt.tight_layout()
    plt.show()

# Generate and plot the Doppler profile
if __name__ == "__main__":
    # Set random seed for reproducible results (optional)
    np.random.seed(42)
    
    # Generate the profile
    time_samples, frequency = generate_doppler_profile()
    
    # Plot the results
    plot_doppler_profile(time_samples, frequency)
    
    # Print some statistics for verification
    print("Doppler Profile Statistics:")
    print("Initial descent (0-800): {:.1f} +/- {:.1f} Hz".format(np.mean(frequency[:800]), np.std(frequency[:800])))
    print("Acceleration peak (1300-1600): {:.1f} +/- {:.1f} Hz".format(np.mean(frequency[1300:1600]), np.std(frequency[1300:1600])))
    print("Pre-parachute (1600-2400): {:.1f} +/- {:.1f} Hz".format(np.mean(frequency[1600:2400]), np.std(frequency[1600:2400])))
    print("Post-parachute (2500-3500): {:.1f} +/- {:.1f} Hz".format(np.mean(frequency[2500:]), np.std(frequency[2500:])))
    
    # Optional: Save data to file
    # np.savetxt('doppler_profile.csv', np.column_stack([time_samples, frequency]), 
    #            delimiter=',', header='Time,Frequency_Hz', comments='')
