# A Python package that wraps CNBC API endpoints and returns financial data in JSON. The API queries business news and live market data to streamline the development of financial applications.

# API KEY - 2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92

import ycnbc

news = ycnbc.News()

# Get trending news
trending_ = news.trending()

# Get latest news
latest_ = news.latest()
print(latest_)
# Get news by category
# economy_ = news.economy()
# jobs_ = news.jobs()
# white_house_ = news.white_house()
# hospitals_ = news.hospitals()
# transportation_ = news.transportation()
# media_ = news.media()
# internet_ = news.internet()
# congress_ = news.congress()
# policy_ = news.policy()
# finance_ = news.finance()
# life_ = news.life()
# defense_ = news.defense()
# europe_politics_ = news.europe_politics()
# china_politics_ = news.china_politics()
# asia_politics_ = news.asia_politics()
# world_politics_ = news.world_politics()
# equity_opportunity_ = news.equity_opportunity()
# politics_ = news.politics()
# wealth_ = news.wealth()
# world_economy_ = news.world_economy()
# central_banks_ = news.central_banks()
# real_estate_ = news.real_estate()
# health_science_ = news.health_science()
# small_business_ = news.small_business()
# lifehealth_insurance_ = news.lifehealth_insurance()
# business_ = news.business()
# energy_ = news.energy()
# industrials_ = news.industrials()
# retail_ = news.retail()
# cybersecurity_ = news.cybersecurity()
# mobile_ = news.mobile()
# technology_ = news.technology()
# cnbc_disruptors_ = news.cnbc_disruptors()
# tech_guide_ = news.tech_guide()
# social_media_ = news.social_media()
# climate_ = news.climate()