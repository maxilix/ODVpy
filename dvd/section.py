from abc import ABC, abstractmethod

from common import *

# 20 dvd sections in order
section_list = ["MISC",
                "BGND",
                "MOVE",
                "SGHT",
                "MASK",
                "WAYS",
                "ELEM",
                "FXBK",
                "MSIC",
                "SND ",
                "PAT ",
                "BOND",
                "MAT ",
                "LIFT",
                "AI  ",
                "BUIL",
                "SCRP",
                "JUMP",
                "CART",
                "DLGS"]

"""
DVM/BGND    Loading map             Chargement de la carte
PAT         Loading updates         Chargement des modifications
ELEM        Loading actors          Chargement des acteurs
MOVE        Loading areas           Chargement des secteurs
MOVE        Loading pathfinder      Chargement du générateur de chemin
SGHT        Loading 3D Elements     Chargement de vision volumétrique
MISC        Loading parameters      Chargement des paramètres spécifiques
BOND        Loading bonds           Chargement des liaisons de zones
FXBK        Loading SFX info        Chargement des sources sonores
MAT         Loading materials       Chargement des matériaux
LIFT        Loading links           Chargement des liaisons verticales
BUIL        Loading buildings       Chargement des batiments
WAYS        Loading waypoints       Chargement des chemins de rondes
SCRP        Loading scripts         Chargement des scripts
AI          Loading AI tactics      Chargement des tactiques d'IA
JUMP        Loading jump zones      Chargement des zones de saut
CART        Loading moving objects  Chargement des objets mobiles
DLGS        Loading dialogues       Chargement des dialogues
MSIC        Loading music           Chargement des musiques
SND         Loading sound           Chargement des sons
WAYS        Loading waypoints       Chargement des chemins de rondes
"""











class Section(RWStreamable):

    _section_name: str
    _section_version: int

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = data
        self._loaded = False
        # log.info(f"Section {self.section} initialized.")

    def __str__(self):
        return f"{self._section_name} Section"

    @property
    def version(self):
        return self._section_version

    @classmethod
    def from_stream(cls, stream):
        name = stream.read(String, 4)
        try:
            assert name == cls._section_name
        except AssertionError:
            raise ValueError(f"Name mismatch: {name} and {cls._section_name}")
        size = stream.read(UInt)
        version = stream.read(Version)
        try:
            assert version == cls._section_version
        except AssertionError:
            raise ValueError(f"{cls._section_name} version mismatch: {version} and {cls._section_version}")
        data = stream.read(Bytes, size - 4)  # minus version size
        return cls(data)

    def load(self, **kwargs):
        substream = ReadStream(self._data)
        self._load(substream, **kwargs)
        next_byte = substream.read(Bytes, 1)
        assert next_byte == b''
        self._loaded = True
        # log.info(f"Section {self.section} loaded")

    @abstractmethod
    def _load(self, substream: ReadStream, **kwargs) -> None:
        # must read (and create) self state from substream
        # can raise an error
        pass

    def to_stream(self, stream):
        if self._loaded:
            self.save()  # update self._data
        stream.write(String(self._section_name))
        stream.write(UInt(len(self._data) + 4))  # plus version size
        stream.write(Version(self._section_version))
        stream.write(Bytes(self._data))

    def save(self):
        substream = WriteStream()
        self._save(substream)
        new_data = substream.get_value()
        if new_data == b'':
            # assume _save() do nothing, self._data dont change
            pass
        else:
            self._data = new_data

    @abstractmethod
    def _save(self, substream: WriteStream) -> None:
        # must write self state in substream
        pass

    @property
    def loaded(self):
        return self._loaded
