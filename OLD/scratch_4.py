op = ops[func]
print(op(*self._add_args(func, opcode)))
# --------------------
"""ops = {
    opcodes.opcode_00e0: lambda _: "CLS",
    opcodes.opcode_annn: lambda _, nnn: f"I = {hex(nnn)}",
}

op = ops[func]
args = {arg: value for arg, value in zip(func.__code__.co_varnames[:func.__code__.co_argcount], self._add_args(func, opcode))}
print(op(**args))"""

# print(func.__code__.co_varnames[:func.__code__.co_argcount])
"""
ops = {
    opcodes.opcode_00e0: lambda **kwargs: "CLS",
    opcodes.opcode_annn: lambda **kwargs: f"I = {hex(nnn)}",
}
op = ops[func]
print(op(*self._add_args(func, opcode)))
"""

"""
# --------------------
mnemo = None
if opcode == 0x00e0:
    mnemo = (lambda sel: "CLS")(*self._add_args(func, opcode))
elif opcode == 0xa248:
    mnemo = (lambda sel, nnn : f"I = {hex(nnn)}")(*self._add_args(func, opcode))
else:
    raise Exception(func, hex(opcode), *self._add_args(func, opcode))
logging.debug(f"model:vm:{hex(self.pc)}:{hex(opcode)}:{mnemo}")

#print(list(*self._add_args(func, opcode)))
#mnemo = "cls"
#logging.debug(f"model:{hex(self.pc)}:{hex(opcode)}:{mnemo}")
# -----------------------------------------------------
"""