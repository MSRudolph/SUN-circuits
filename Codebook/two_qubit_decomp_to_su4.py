import pennylane as qml
import numpy as np
from qiskit.quantum_info import *
from scipy.linalg import logm

# Define the Pauli matrices
I = np.eye(2)  # Identity matrix
sigma_x = np.array([[0, 1], [1, 0]])  # Pauli X matrix
sigma_y = np.array([[0, -1j], [1j, 0]])  # Pauli Y matrix
sigma_z = np.array([[1, 0], [0, -1]])  # Pauli Z matrix

# Define the extended Pauli basis for two qubits
pauli_basis = {
    'IX': np.kron(I, sigma_x), 'IY': np.kron(I, sigma_y), 'IZ': np.kron(I, sigma_z),
    'XI': np.kron(sigma_x, I), 'XX': np.kron(sigma_x, sigma_x), 'XY': np.kron(sigma_x, sigma_y), 'XZ': np.kron(sigma_x, sigma_z),
    'YI': np.kron(sigma_y, I), 'YX': np.kron(sigma_y, sigma_x), 'YY': np.kron(sigma_y, sigma_y), 'YZ': np.kron(sigma_y, sigma_z),
    'ZI': np.kron(sigma_z, I), 'ZX': np.kron(sigma_z, sigma_x), 'ZY': np.kron(sigma_z, sigma_y), 'ZZ': np.kron(sigma_z, sigma_z)
}

def extract_pauli_coeff(U, threshold=1e-6):
    """
    Extract the coefficients of the Pauli matrices from the matrix logarithm of U.

    Args:
        U (np.ndarray): The unitary matrix.
        threshold (float): The threshold below which coefficients are set to zero.

    Returns:
        dict: A dictionary containing the coefficients of the Pauli matrices.
    """
    # Compute the Hermitian matrix H from the matrix logarithm of U
    H = logm(U)

    # Calculate the coefficients for each Pauli matrix in the basis
    coefficients = {}
    for key, Pk in pauli_basis.items():
        coeff = np.trace(H @ Pk) / 4

        # Set coefficients below the threshold to zero
        if abs(coeff.real) < threshold:
            coeff = complex(0, coeff.imag)
        if abs(coeff.imag) < threshold:
            coeff = complex(coeff.real, 0)
        coefficients[key] = coeff

    return coefficients

def two_qubit_decomp_1(params, wires):
    """
    Implement an arbitrary SU(4) gate on two qubits using a specific decomposition.

    Args:
        params (list): A list of 15 parameters for the decomposition.
        wires (list): The two qubits on which the gate acts.
    """
    i, j = wires    
    qml.RZ(params[0], wires=i)
    qml.RY(params[1], wires=i)
    qml.RZ(params[2], wires=i)
    qml.RZ(params[3], wires=j)
    qml.RY(params[4], wires=j)
    qml.RZ(params[5], wires=j)
    qml.CNOT(wires=[j, i])
    qml.RZ(params[6], wires=i)
    qml.RY(params[7], wires=j)
    qml.CNOT(wires=[i, j])
    qml.RY(params[8], wires=j)
    qml.CNOT(wires=[j, i])
    qml.RZ(params[9], wires=j)
    qml.RY(params[10], wires=j)
    qml.RZ(params[11], wires=j)
    qml.RZ(params[12], wires=i)
    qml.RY(params[13], wires=i)
    qml.RZ(params[14], wires=i)

# Define the device
dev = qml.device('default.qubit', wires=2)

# Wrap the circuit in a QNode
@qml.qnode(dev)
def circuit1(params):
    """
    Define a quantum circuit using the two-qubit decomposition.

    Args:
        params (list): A list of 15 parameters for the SU(4) decomposition.

    Returns:
        np.ndarray: The final quantum state of the system.
    """
    two_qubit_decomp_1(params, wires=[0, 1])
    return qml.state()

def rev_map(init_pauli_params):
    """
    Reverse map the initial Pauli parameters to the SU(4) coefficients.

    Args:
        init_pauli_params (list): Initial parameters for the Pauli decomposition.

    Returns:
        np.ndarray: The coefficients of the SU(4) decomposition.
    """
    # Extract the unitary matrix from the quantum circuit
    U_rot = qml.matrix(circuit1)(init_pauli_params)

    # Extract the coefficients for the Pauli matrices
    coeff_Urot = extract_pauli_coeff(U_rot)

    # Normalize the coefficients for the SU(4) group
    coeff_SU4 = [elem / 1j for elem in coeff_Urot.values()]

    return np.array(coeff_SU4)
