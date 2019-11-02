# logging mnemonics taken from cowgod's chip8 tech ref -- TODO: add thanks

# TODO: verify accordance to "mastering the chip8"
# TODO: yes, the logging reduces speed -- consider this later... decorator applied by vm? -- afects args?
# TODO: a decorator would work


"""
# Call opcode

# Conditional opcodes



# Const opcodes

# Display opcodes



# KeyOp opcodes



# Math opcodes
@increment_pc

# Memory opcodes


# Random opcodes



"""







if __name__ == "__main__":
    vm.load_program("Chip8 Picture.ch8")
    vm.run()
    print(vm.screen.dump_textshot())


