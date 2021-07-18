# Arithmetic Coding Algorithm

Implementation of a text compression arithmetic encoder using a static model and integer arithmetic.

Usage:
> python3 arco.py filename

Notes:

- The encoder uses the bitstream.BitStream class to store the generated code, but it doesn't save the code to a file, it just prints the output of the ArithmeticCoding.encode method if ArithmeticCoding.debug is enabled.

Next Steps:

- Find a way to save the generated code to a file (efficiently).
- Add ArithmeticCoding.decode method.
- Add optional support for adaptive arithmetic coding.