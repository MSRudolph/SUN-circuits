# max_cut.py
import numpy as np
from qiskit.quantum_info import SparsePauliOp
import pennylane as qml

def max_cut():
    # Set up the number of qubits and wires
    num_wires = 4
    wires = list(range(num_wires))
    np.random.seed(62213)

    # Define the Hamiltonian using SparsePauliOp
    hamiltonian = SparsePauliOp.from_list([
        ("IIZZ", 1), ("ZIZI", 1), ("IZZI", 1), ("ZIIZ", 1), ("ZZII", 1)
    ])

    # Convert the SparsePauliOp to a matrix
    H_matrix = hamiltonian.to_matrix()
    H = qml.Hermitian(H_matrix, wires=wires)

    # Compute the eigenvalues and eigenvectors of the Hamiltonian
    eigenvalues, eigenvectors = np.linalg.eigh(H_matrix)

    # Add noise to the eigenvalues
    
    noise = np.random.randn(eigenvalues.shape[0]) * 10  # Adjust noise scale as needed
    noisy_eigenvalues = eigenvalues + noise

    # Reconstruct the noisy Hamiltonian using the noisy eigenvalues and original eigenvectors
    noisy_H_matrix = eigenvectors @ np.diag(noisy_eigenvalues) @ np.linalg.inv(eigenvectors)
    noisy_H = qml.Hermitian(noisy_H_matrix, wires=wires)

    # Compute the ground state energy of the noisy Hamiltonian
    E_min_noisy = min(qml.eigvals(noisy_H))
    print(f"Noisy ground state energy: {E_min_noisy:.5f}")

    # Optional: Print the noisy eigenvalues
    print("Noisy eigenvalues:", qml.eigvals(noisy_H))

    return noisy_H

# if __name__ == "__main__":
#     noisy_H = main()
