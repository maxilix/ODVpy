import json
import os

TRANSPARENTS = [(0, 248, 0), (0, 0, 248)]
TRANSPARENT_GREEN = TRANSPARENTS[0]
TRANSPARENT_BLUE = TRANSPARENTS[1]

# GAME_PATH = "../Desperados Wanted Dead or Alive"

ORIGINAL_HASH = {
    f"data{os.sep}levels{os.sep}level_01.dvd":
        "98e8e3fa2473d056646f66833f240a325e486b6713f34cf056b6fa1e8bb790f0",
    f"data{os.sep}levels{os.sep}level_01.scb":
        "f554d838b9959b32b8a3e1031e2d3c88623e40ce51e7f916193f62b34fbced15",
    f"data{os.sep}levels{os.sep}level_02.dvd":
        "55f02062b691906ba1786a8acf4fd3c2223b039659da957cbd5a1324c9dec60d",
    f"data{os.sep}levels{os.sep}level_02.scb":
        "e8f4835ac148bb57763ecd64b7df8864e348601320faa18522f813966407d2d5",
    f"data{os.sep}levels{os.sep}level_03.dvd":
        "dc573eb314b929d192146e5b46c6721d36ecf9eac627e3403f63cf021ee3cc5a",
    f"data{os.sep}levels{os.sep}level_03.scb":
        "a789d544da131fc26f6639cc3bdaca7ecfc8195196d706169eb8221dab18f993",
    f"data{os.sep}levels{os.sep}level_04.dvd":
        "5601904d20acdad052a0bf1b402093b2b587c1d086b51b65551f8201ceaf3907",
    f"data{os.sep}levels{os.sep}level_04.scb":
        "2cfeb03d411aeb048acfbf844bab04efe9ba4c69acfd03a5444bbc175428fd27",
    f"data{os.sep}levels{os.sep}level_05.dvd":
        "4625cfc6fe32ca7cfd4845ef7fb6916a078b0a3aa4f4f88580b794a53c69ddd9",
    f"data{os.sep}levels{os.sep}level_05.scb":
        "427ce5c15ebbd54e692fbdf45227df0e87a9211888b6700a10fd782fa974fb9c",
    f"data{os.sep}levels{os.sep}level_06.dvd":
        "61e802a4ddc6b15c9512e20b940850d900738973e5f65da801b8e4bd0932abb2",
    f"data{os.sep}levels{os.sep}level_06.scb":
        "bcad594d9264ff85aebd4347e4de1ae83953278939a32de874f8823e8503ee17",
    f"data{os.sep}levels{os.sep}level_07.dvd":
        "fd30a51f3147a19602ef85fb5727d42877f58cd1c263ce8a5c8c1494298d67b9",
    f"data{os.sep}levels{os.sep}level_07.scb":
        "081766c67144fdfcc419909940196fb33c0d6f65c3491587607e6b8388df50dd",
    f"data{os.sep}levels{os.sep}level_08.dvd":
        "8c38f6dbe9026c6d548277f4c314c0eab9e5703719a2c753e0599c354026525c",
    f"data{os.sep}levels{os.sep}level_08.scb":
        "dd0f409632eb964faf3d1cfd445722968a2bc4e0f896941545e0a70736fb9fd2",
    f"data{os.sep}levels{os.sep}level_09.dvd":
        "8930b388fc5469c91d98a262c3caecdcf88f46dffd37bbc3c0fb1f42929be11d",
    f"data{os.sep}levels{os.sep}level_09.scb":
        "5c487b2becbaef1be9e879ea4d34bd347771cdf5523edf8207a5bf61c2176abc",
    f"data{os.sep}levels{os.sep}level_10.dvd":
        "86842da67e05fbd306921da45fab9ba0045df03e5f090d6401770706db7cac8c",
    f"data{os.sep}levels{os.sep}level_10.scb":
        "7ff5c90bffe3ece345db30d499bee0357d9757f028763cb49ca4329be52dc5d0",
    f"data{os.sep}levels{os.sep}level_11.dvd":
        "9e675e0180df9c09cb7f7f404fb7b55284f5f6dbc21f157c98302b5bcba5e72c",
    f"data{os.sep}levels{os.sep}level_11.scb":
        "8cb856130a172b55fef9afb4ec26f33ccf311fd1095080fd77b1c7e1e635991d",
    f"data{os.sep}levels{os.sep}level_12.dvd":
        "1b7a0ca73683e75e5a2be84d0483e14b3b2ca3926d8efe9b2ec9fce5eff42f3f",
    f"data{os.sep}levels{os.sep}level_12.scb":
        "68baf22ec84c71995dd878f1f69577e3528c703f94692d3536f9e6b294b548fd",
    f"data{os.sep}levels{os.sep}level_13.dvd":
        "14d35272c05dd7386fe7818093d4690afe49aa778be51ac901fcd3fa74dca833",
    f"data{os.sep}levels{os.sep}level_13.scb":
        "7f5df1d554b565f2197eed743f6840843922c2b9bb75ccab16ecf3712a078975",
    f"data{os.sep}levels{os.sep}level_14.dvd":
        "ecca5b68cd4dc3697ff9d688c899935d49ea4fa2ea35b79c36dc78a38c1757e5",
    f"data{os.sep}levels{os.sep}level_14.scb":
        "f916e329bd4f12fbb1be50b9b27c3bd4259365f9b1bcc6d757beb413a3c2c0b6",
    f"data{os.sep}levels{os.sep}level_15.dvd":
        "aebbd757ed0661dee49993a8e7f54e913d1a47f81a51d8e38b19d1e5e8b2cdb8",
    f"data{os.sep}levels{os.sep}level_15.scb":
        "65e1327e7b5c42c12f0f979a4e677bafb8ff1c6b7cccf5ff4d2465677f85469f",
    f"data{os.sep}levels{os.sep}level_16.dvd":
        "e5971fa28ec8776b2064cf7dc24e26dd18933a91042b9df9fe99b922fe11cce0",
    f"data{os.sep}levels{os.sep}level_16.scb":
        "31afbc8ee8ed2a6c6e88d0dc4ee51543ec275d9737c579ee4064bfa0d38e3d7f",
    f"data{os.sep}levels{os.sep}level_17.dvd":
        "d4a843cbb93b0abb794c37c6b7b105d31365532bcc888043613a4efd55004b77",
    f"data{os.sep}levels{os.sep}level_17.scb":
        "97f6c86933bb7c37c275944f7572e5361b348c4ff7f9e279cc0719f919372a9d",
    f"data{os.sep}levels{os.sep}level_18.dvd":
        "5c119b428c00a0e0e53ea6a918efa5cafb976abae08bf058ba80a4b427b0567f",
    f"data{os.sep}levels{os.sep}level_18.scb":
        "b72797d61784232212a9046060f9b228726088acf2e80941e036272bf28559c4",
    f"data{os.sep}levels{os.sep}level_19.dvd":
        "104f2b4c1888a6312f435a35962f62d2a7957dbf930bbea9d64eb991abad68ec",
    f"data{os.sep}levels{os.sep}level_19.scb":
        "529dc45a4bcfb8e75ad586f05c2d526f73417bf9c329c1504a89c86e3b66d228",
    f"data{os.sep}levels{os.sep}level_20.dvd":
        "f63ad75faf504fd5f4088903e9ff97cb0c29e8258fc3b6dc0146b56b7388a894",
    f"data{os.sep}levels{os.sep}level_20.scb":
        "690192894c066a36a642a66cfb5c04b809cde75ee70b959aab5c7cd9e5f7f911",
    f"data{os.sep}levels{os.sep}level_21.dvd":
        "04b65c6704afdacaafd1ebbd2f0579057d45cd38fd8b4730d0cec972ab22eb9c",
    f"data{os.sep}levels{os.sep}level_21.scb":
        "537accf9be3b4e685d7db46f550fb7531505f12234b3695b6714a8293797f8dd",
    f"data{os.sep}levels{os.sep}level_22.dvd":
        "071b9415e747c1d1dbdffc2022ae800509180703d29035c438a7a21ec5996ba0",
    f"data{os.sep}levels{os.sep}level_22.scb":
        "6b68e5a1a0ff646cc7902001473912634f818125afdac3073e0e7ac33d63a9e1",
    f"data{os.sep}levels{os.sep}level_23.dvd":
        "3640ee9026c06253cc9f875dcb033a6cc38f930f194672f0c1ae249311956a84",
    f"data{os.sep}levels{os.sep}level_23.scb":
        "89fc95792effafdc478a2eff16e0e8fef6490eea65d6528ffe55c93b713c6f11",
    f"data{os.sep}levels{os.sep}level_24.dvd":
        "f4e1f270e2b5c5a974be22728375cacbb16f44a08470936ad36ee3118c3313de",
    f"data{os.sep}levels{os.sep}level_24.scb":
        "a6df6b4ea9ed76293ed4e0157386090cbd2ff68734d61732450d02be70098a5f",
    f"data{os.sep}levels{os.sep}level_25.dvd":
        "1f25208aa47ed41e473f331511c8060b3d5c4e75b629d5d8ef3f97fe68fb877a",
    f"data{os.sep}levels{os.sep}level_25.scb":
        "52108b0136c98cb5312f09fc7a8c6faef3ae9bb94cdc06282d535361a25a4a6e",
    f"demo{os.sep}data{os.sep}levels{os.sep}level_00.dvd":
        "a2b3cc0a0cd0e56548f03377e87d1385498e50ea0f333c766d219e694a0b279d",
    f"demo{os.sep}data{os.sep}levels{os.sep}level_00.scb":
        "5d9005a6ba4aeaabb4737d658ddf1935694af4d32a42b83afe2f1e9bee267be7"}

CONFIG_FILENAME = "config.json"


class CONFIG(object):
    installation_path = ""

    @classmethod
    def load(cls):
        with open(CONFIG_FILENAME, "r") as json_file:
            data = json.load(json_file)
        cls.installation_path = data["installation_path"]

    @classmethod
    def save(cls):
        data = dict()
        data["installation_path"] = cls.installation_path
        with open(CONFIG_FILENAME, "w") as json_file:
            json.dump(data, json_file)


def original_level_filename(index):
    assert 0 <= index <= 25
    filename = CONFIG.installation_path
    if index == 0:
        filename += f"{os.sep}demo"
    filename += f"{os.sep}data{os.sep}levels{os.sep}level_{index:02}"
    return filename


class OriginalMission(object):

    def __init__(self, index):
        assert 0 <= index <= 25
        self.index = index
        # self.dvd_filename =

        filename = CONFIG.installation_path
        if index == 0:
            filename += f"{os.sep}demo"
        filename += f"{os.sep}data{os.sep}levels{os.sep}level_{index:02}"
