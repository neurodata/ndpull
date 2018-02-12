from ndpull import sliceDownload

collection = 'kharris15'
experiment = 'apical'
channel = 'em'

# see neurodata.cfg.example to generate your own
config_file = 'neurodata.cfg'

# print metadata
meta = sliceDownload.BossMeta(collection, experiment, channel)
token, boss_url = sliceDownload.get_boss_config(config_file)
rmt = sliceDownload.BossRemote(boss_url, token, meta)
print(rmt)

# download slices with these limits:
x = [0, 512]
y = [500, 1000]
z = [0, 10]

# returns a namespace as a way of passing arguments
result = sliceDownload.parse_input_args(
    collection, experiment, channel, config_file, x=x, y=y, z=z, res=0, outdir='./')

# downloads the data
sliceDownload.download_slices(result, rmt)
