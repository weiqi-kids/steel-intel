"""
公司新聞爬蟲
"""

from .base import CompanyFetcher, CompanyDocument

from .arcelormittal import ArcelormittalFetcher
from .baosteel import BaosteelFetcher
from .bhp import BhpFetcher
from .china_steel import ChinaSteelFetcher
from .chung_hung import ChungHungFetcher
from .cleveland_cliffs import ClevelandCliffsFetcher
from .cmc import CmcFetcher
from .feng_hsin import FengHsinFetcher
from .fortescue import FortescueFetcher
from .gerdau import GerdauFetcher
from .hyundai_steel import HyundaiSteelFetcher
from .jfe import JfeFetcher
from .nippon_steel import NipponSteelFetcher
from .nucor import NucorFetcher
from .posco import PoscoFetcher
from .reliance import RelianceFetcher
from .rio_tinto import RioTintoFetcher
from .spring_rain import SpringRainFetcher
from .steel_dynamics import SteelDynamicsFetcher
from .suncoke import SuncokeFetcher
from .ta_chen import TaChenFetcher
from .tata_steel import TataSteelFetcher
from .tenaris import TenarisFetcher
from .tung_ho import TungHoFetcher
from .us_steel import UsSteelFetcher
from .vale import ValeFetcher
from .warrior_met import WarriorMetFetcher

FETCHERS = {
    "arcelormittal": ArcelormittalFetcher,
    "baosteel": BaosteelFetcher,
    "bhp": BhpFetcher,
    "china_steel": ChinaSteelFetcher,
    "chung_hung": ChungHungFetcher,
    "cleveland_cliffs": ClevelandCliffsFetcher,
    "cmc": CmcFetcher,
    "feng_hsin": FengHsinFetcher,
    "fortescue": FortescueFetcher,
    "gerdau": GerdauFetcher,
    "hyundai_steel": HyundaiSteelFetcher,
    "jfe": JfeFetcher,
    "nippon_steel": NipponSteelFetcher,
    "nucor": NucorFetcher,
    "posco": PoscoFetcher,
    "reliance": RelianceFetcher,
    "rio_tinto": RioTintoFetcher,
    "spring_rain": SpringRainFetcher,
    "steel_dynamics": SteelDynamicsFetcher,
    "suncoke": SuncokeFetcher,
    "ta_chen": TaChenFetcher,
    "tata_steel": TataSteelFetcher,
    "tenaris": TenarisFetcher,
    "tung_ho": TungHoFetcher,
    "us_steel": UsSteelFetcher,
    "vale": ValeFetcher,
    "warrior_met": WarriorMetFetcher,
}
