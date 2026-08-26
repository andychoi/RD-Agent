import qlib

qlib.init(provider_uri="~/.qlib/qlib_data/us_sp500_alpaca", region="us")

from qlib.data import D

instruments = D.instruments("sp500")
fields = ["$open", "$close", "$high", "$low", "$volume", "$factor"]
data = (
    D.features(instruments, fields, start_time="2020-07-27", end_time="2024-12-31", freq="day")
    .swaplevel()
    .sort_index()
)

data.to_hdf("./daily_pv_all.h5", key="data")


fields = ["$open", "$close", "$high", "$low", "$volume", "$factor"]
data = (
    (
        D.features(instruments, fields, start_time="2023-01-03", end_time="2024-12-31", freq="day")
        .swaplevel()
        .sort_index()
    )
    .swaplevel()
    .loc[data.reset_index()["instrument"].unique()[:100]]
    .swaplevel()
    .sort_index()
)

data.to_hdf("./daily_pv_debug.h5", key="data")
