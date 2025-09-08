# Mars EDL Doppler Tracking Simulation

This application simulates Mars Entry, Descent, and Landing (EDL) Doppler frequency tracking using Geometric Algebra-based Least Mean Squares (GA-LMS) algorithms. It compares the performance of GA-LMS against traditional epsilon-Normalized Least Mean Squares (ε-NLMS) adaptive filtering for signal tracking during critical Mars landing phases.

## Notes for Publication

### TODO

- we need to implement the prediction-error filter and apply that to the GA-LMS in order to have the right frequency vs sample curves plotted. See paper ssp_2007_a.pdf for the prediction-error filter.

### Research Focus and Angles

**Primary Research Contribution**: Demonstrating GA-LMS computational scalability advantages for Doppler tracking applications.

**Key Technical Angles**:

1. **Computational Complexity Advantage**
   - GA-LMS: O(1) complexity - **independent of filter order M**
   - e-NLMS: O(M) complexity - scales linearly with filter order  
   - **Memory Efficiency**: GA-LMS uses constant 8 real numbers vs e-NLMS 4×M numbers
   - **Crossover Analysis**: GA-LMS becomes advantageous for M > ~10 (based on complexity analysis)

2. **Scalability for High-Order Systems**
   - Traditional adaptive filters become computationally prohibitive for large M
   - GA-LMS maintains constant computational cost regardless of system complexity
   - **Space Applications**: Critical for power-constrained Mars EDL systems requiring high precision

3. **Theoretical Foundation**
   - **Geometric Algebra Framework**: Bounded parameter updates through rotor normalization
   - **Multivector Operations**: Natural representation of complex signal rotations
   - **Inherent Stability**: Geometric constraints prevent parameter drift

**Research Direction Suggestions**:

- **Focus on scalability benefits** rather than marginal performance improvements
- Emphasize **constant memory footprint** as major advantage for embedded systems
- Position GA-LMS as **future-proof solution** for increasingly complex Mars missions
- Highlight **power efficiency** implications for Mars EDL communications

**Publication Strategy**:
- Lead with computational complexity analysis showing O(1) vs O(M) scaling
- Demonstrate memory efficiency advantages for space applications  
- Use Mars EDL as compelling application domain requiring both precision and efficiency
- Position tracking capability as secondary benefit, not primary contribution

**Potential Limitations to Address**:
- Higher base computational cost for very small filter orders (M < 10)
- Implementation complexity compared to traditional LMS variants
- Need for geometric algebra mathematical framework understanding

**Future Work Directions**:
- Hardware implementation comparisons (FPGA/DSP)
- Power consumption analysis for space-qualified processors
- Integration with existing Mars EDL communication systems
- Extension to multi-dimensional tracking scenarios

## Overview

The simulation models the complex Doppler frequency profile encountered during Mars EDL operations, including:
- Initial descent phase
- Acceleration build-up 
- Peak acceleration during atmospheric entry
- Pre-parachute dynamics
- Parachute deployment
- Final descent to landing

The system generates synthetic Mars EDL signals and processes them using both GA-LMS and ε-NLMS algorithms to evaluate tracking performance during these critical mission phases.

## Prerequisites

### Dependencies

Install the required Python packages:

```bash
pip install -r ogre_dir/requirements.txt
```

Required packages:
- numpy (2.2.6)
- matplotlib (3.10.3)
- Additional dependencies as specified in `ogre_dir/requirements.txt`

### Binary Compilation

The GA-LMS algorithm is implemented in C++ and must be compiled before running the simulation. The binary is located at:
```
../../src/GAAFs_doppler/doppler_galms/build/doppler_galms
```

If the binary doesn't exist, you'll need to compile it first using the provided CMake configuration in the upstream directory.

## Usage

### Running the Main Simulation

Execute the main simulation script:

```bash
python doppler_tracking_testbench.py
```

### Advanced Analysis Suite

For comprehensive algorithm analysis including tracking capability and outlier robustness:

```bash
python outliers_doppler_tracking_testbench.py
```

This enhanced analysis suite provides:
- **Tracking Capability Assessment**: Algorithm response to abrupt Doppler changes
- **Outlier Robustness Analysis**: Performance under signal corruption
- **Computational Complexity Comparison**: Efficiency metrics and scaling analysis
- **Theoretical Performance Analysis**: Mathematical foundations and algorithmic differences

### Simulation Parameters

The simulation uses the following default parameters (configured in `doppler_tracking_testbench.py`):

- **System order (M)**: 4 taps
- **Realizations (L)**: 10 
- **Time iterations (N)**: 3500 samples
- **Step size (μ)**: 1e-3
- **Noise variance (σ²v)**: 1e-2  
- **Sampling frequency**: 100 Hz
- **Acceleration peak time**: Sample 1000
- **Parachute deployment time**: Sample 2500

### Generated Files

The simulation generates several output files:

**Input Signals:**
- `input_signal.txt` - Average input signal for C++ processing
- `input_signal_real_0.txt` to `input_signal_real_9.txt` - Individual realization signals

**Algorithm Outputs:**
- `MSE_new_filter.out` - GA-LMS Mean Squared Error values
- `x_estimated.out` - GA-LMS signal estimates
- `x_input.out` - Input signal verification
- `final_rotor.out` - Final rotor coefficients

**Results:**
- `mars_edl_signal_tracking_comparison.pdf` - Comprehensive performance analysis plots

**Advanced Analysis Outputs (from `outliers_doppler_tracking_testbench.py`):**
- `tracking_capability_analysis.pdf` - Tracking capability assessment with abrupt changes
- `mars_edl_algorithm_comparison.pdf` - Outlier robustness analysis
- `mars_edl_comprehensive_analysis.pdf` - Computational complexity and theoretical analysis

## Output Analysis

### Basic Simulation Analysis

The main simulation provides detailed performance comparisons including:

1. **Signal Tracking Comparison**: Real and imaginary parts, magnitude, and phase tracking
2. **Learning Curves**: MSE evolution for both algorithms
3. **Critical Period Analysis**: Performance during acceleration peak and parachute deployment
4. **Cumulative Performance Metrics**: Long-term algorithm behavior

### Advanced Analysis Suite

The enhanced analysis provides comprehensive algorithm evaluation:

#### Tracking Capability Assessment
- **Transient Response Analysis**: Algorithm adaptation speed to abrupt changes
- **Change Detection Performance**: How quickly algorithms detect signal changes
- **Recovery Metrics**: Error reduction rates after disturbances
- **Steady-State Performance**: Final tracking accuracy after changes

#### Test Scenarios for Tracking Capability
1. **Step Changes**: Abrupt frequency jumps simulating sudden trajectory changes
2. **Ramp Changes**: Rapid acceleration/deceleration phases
3. **Frequency Switching**: Sudden oscillation pattern changes
4. **EDL Interference Bursts**: Mars EDL with sudden interference events

#### Outlier Robustness Analysis
- **Spike Tolerance**: Response to isolated frequency spikes
- **Burst Interference**: Performance under sustained interference
- **Noise Resilience**: Behavior in varying noise conditions

#### Computational Analysis
- **Complexity Scaling**: Performance vs filter order relationships
- **Memory Requirements**: Resource usage comparison
- **Efficiency Metrics**: Operations per iteration analysis

### Performance Metrics

The system reports comprehensive metrics:
- **Basic Metrics**: MSE, MAE, improvement percentages
- **Tracking Metrics**: Transient times, detection delays, recovery rates  
- **Robustness Metrics**: Outlier impact, performance degradation
- **Efficiency Metrics**: Computational complexity, memory usage

## Algorithm Details

### GA-LMS (Geometric Algebra LMS)
- Processes complex signals using geometric algebra operations
- Implemented in C++ for computational efficiency
- Uses rotor-based multivector operations for signal estimation
- Features bounded parameter updates through geometric constraints

### ε-NLMS (Epsilon-Normalized LMS)
- Traditional adaptive filtering approach
- Python implementation included for comparison
- Uses normalized gradient descent with regularization
- Linear coefficient update mechanism

## File Structure

```
Doppler_tracking/
├── doppler_tracking_testbench.py              # Main simulation script
├── outliers_doppler_tracking_testbench.py     # Advanced analysis suite
├── abstract.md                                # Paper abstract
├── README.md                                  # This documentation
├── ogre_dir/
│   └── requirements.txt                       # Python dependencies
├── support_papers/                            # Reference papers
│   ├── 1601.06044v1.pdf                      # GA-LMS theory
│   ├── 1608.03450v2.pdf                      # GA adaptive filters
│   ├── asilomar_2006_b.pdf                   # Mars EDL tracking
│   └── ssp_2007_a.pdf                        # Enhanced EDL tracking
├── input_signal*.txt                          # Generated input signals
├── *.out                                     # Algorithm output files  
├── mars_edl_signal_tracking_comparison.pdf    # Basic results
├── tracking_capability_analysis.pdf           # Tracking capability assessment
├── mars_edl_algorithm_comparison.pdf          # Outlier robustness analysis
├── mars_edl_comprehensive_analysis.pdf       # Full theoretical analysis
└── logs/                                      # Execution logs for analysis
    ├── doppler_tracking_testbench_*.log       # Main simulation logs
    └── outliers_testbench_*.log               # Advanced analysis logs
```

## Logging and Analysis

All simulation runs generate comprehensive logs in the `logs/` directory with timestamps. These logs contain:

- **Simulation Parameters**: All configuration values and settings
- **Processing Steps**: Detailed execution flow and intermediate results
- **Performance Metrics**: MSE values, computational statistics, timing information
- **Error Handling**: Any issues with binary execution or file I/O
- **Results Summary**: Final performance comparisons and key insights
- **Publication Insights**: Automatically generated observations for research analysis

Log files are named with timestamps (YYYYMMDD_HHMMSS) for easy identification and can be used for:
- Reproducing exact simulation conditions
- Analyzing performance trends across multiple runs
- Debugging simulation issues
- Extracting quantitative results for publications

## Troubleshooting

### Common Issues

1. **Binary not found**: Ensure the GA-LMS binary is compiled and exists at the specified path
2. **Missing dependencies**: Install required packages using `pip install -r ogre_dir/requirements.txt`
3. **Permission errors**: Ensure the binary has execute permissions
4. **Memory issues**: Reduce the number of iterations (N) or realizations (L) for large simulations

### Output Files Missing

If the C++ binary fails to execute, the simulation will continue with ε-NLMS results only. Check:
- Binary file exists and has execute permissions
- All required input files are generated properly
- Sufficient disk space for output files

## Mars EDL Context

This simulation is based on real Mars EDL mission profiles and addresses the critical communication challenges during Mars landing operations. The Doppler tracking capabilities are essential for:
- Real-time trajectory monitoring
- Landing site accuracy
- Mission success verification

The simulation parameters and frequency profiles are derived from actual Mars EDL mission data and research publications in the field of Mars exploration communications.
