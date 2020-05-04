from elftools.elf.elffile import ELFFile

class reader:
    def __init__(self, elffile):
        self._elf = ELFFile(open(elffile, 'rb'))
        self._symtab = self._elf.get_section_by_name('.symtab')

    def getAddressOfSym(self, symbol_name):
        addr = None

        if not self._symtab is None:
            sym = self._symtab.get_symbol_by_name(symbol_name)[0]
            if not sym is None:
                addr = sym.entry.st_value
        
        return addr

    def getSizeOfSym(self, symbol_name):
        size = None

        if not self._symtab is None:
            sym = self._symtab.get_symbol_by_name(symbol_name)[0]
            if not sym is None:
                size = sym.entry.st_size
        
        return size