from copy import deepcopy

from core.bin_streams import BinArchiveWriter, BinArchiveReader
from module.module import Module
from module.properties.pointer_property import PointerProperty


class ObjectModule(Module):
    def __init__(self, js):
        super().__init__(js)
        self.element = deepcopy(self.element_template)

    def find_base_address_for_element(self, element):
        if not self.archive:
            raise ValueError
        if element != self.element:
            raise ValueError
        return self.location_strategy.read_base_address(self.archive)

    def attach_to(self, archive):
        location = self.location_strategy.read_base_address(archive)
        reader = BinArchiveReader(archive, location)
        for prop in self.element.values():
            prop.read(reader)
        self.archive = archive

    def commit_changes(self):
        location = self.location_strategy.read_base_address(self.archive)
        writer = BinArchiveWriter(self.archive, location)
        for prop in self.element.values():
            prop.write(writer)

    def update_post_shallow_copy_fields(self):
        self.element = deepcopy(self.element_template)
        for prop in self.element_template.values():
            if type(prop) == PointerProperty:
                prop.module = self
