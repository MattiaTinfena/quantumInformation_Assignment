from qiskit import QuantumCircuit
from qiskit_aer import Aer 
from qiskit import transpile
import random

key_len_bytes = 4
key_len_bit = key_len_bytes * 8

key_sender = [random.randint(0,1) for _ in range(key_len_bit)]
base_sender = [random.randint(0,1) for _ in range(key_len_bit)]
base_receiver = [random.randint(0,1) for _ in range(key_len_bit)]
receiver_results = []

#run the simulator
backend = Aer.get_backend('qasm_simulator')


for i in range(key_len_bit):
    qc = QuantumCircuit(1,1)
    if base_sender[i] == 0:
        if key_sender[i] == 1:
            qc.x(0)
    else:
        qc.h(0)
        if key_sender[i] == 1:
            qc.z(0)
    if base_receiver[i] == 1:
        qc.h(0)

    qc.measure(0,0)

    new_cirq = transpile(qc,backend)
    job = backend.run(new_cirq, shots=1)
    
    counts = job.result().get_counts()

    measured_bit = int(list(counts.keys())[0])
    receiver_results.append(measured_bit)

sifted_sender = []
sifted_receiver = []

for i in range(key_len_bit):
    if base_sender[i] == base_receiver[i]:
        sifted_sender.append(key_sender[i])
        sifted_receiver.append(receiver_results[i])        
        print(f"Qbit {i}: Basis match({base_sender[i]}). Sender bit: {key_sender[i]}, recived measurement: {receiver_results[i]}")    
    else:
        print(f"Qbit {i}: Basis mismatch({base_sender[i]}). Sender bit: {key_sender[i]}, recived measurement: {receiver_results[i]}")    

errors = sum(1 for a,b in zip(sifted_sender, sifted_receiver) if a != b)
error = errors / len(sifted_sender) if sifted_sender else 0

print("\nFinal sifted key sender:",sifted_sender)
print("\nFinal sifted key receiver:",sifted_receiver)
print(f"\nError: {error *100:.2f}%")

