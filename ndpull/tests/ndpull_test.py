from ndpull.ndpull import *


class Testndpull():

    def test_print_meta(self):
        meta = BossMeta('lee', 'lee14', 'image')

        token, boss_url = get_boss_config('neurodata.cfg')
        rmt = BossRemote(boss_url, token, meta)
        print(rmt)

    def test_no_token(self):
        result = argparse.Namespace(
            config_file=None,
            token=None,
        )
        with pytest.raises(ValueError, message='Need token or config file'):
            validate_args(result)

    def test_wrong_extents(self):
        result = argparse.Namespace(
            x=[0, 512],
            y=[500, 1000],
            z=[-1, 10],
            config_file='neurodata.cfg',
            collection='lee',
            experiment='lee14',
            channel='image',
            print_metadata=None,
            full_extent=None,
        )
        with pytest.raises(ValueError):
            validate_args(result)

    def test_create_rmt(self):
        result = argparse.Namespace(
            x=[0, 512],
            y=[500, 1000],
            z=[0, 10],
            config_file='neurodata.cfg',
            collection='lee',
            experiment='lee14',
            channel='image',
            print_metadata=None,
            full_extent=None,
        )
        result, rmt = validate_args(result)

        assert rmt.meta.collection() == result.collection
        assert rmt.meta.experiment() == result.experiment
        assert rmt.meta.channel() == result.channel

    def test_small_cutout(self):
        result = argparse.Namespace(
            x=[0, 512],
            y=[500, 1000],
            z=[15, 22],
            config_file='neurodata.cfg',
            collection='lee',
            experiment='lee14',
            channel='image',
            print_metadata=None,
            full_extent=None,
        )
        datatype = 'uint8'

        result, rmt = validate_args(result)

        cutout_url_base = "{}/{}/cutout/{}/{}/{}".format(
            result.url, BOSS_VERSION, result.collection, result.experiment, result.channel)
        cutout_url = "{}/{}/{}:{}/{}:{}/{}:{}/".format(
            cutout_url_base, 0, result.x[0], result.x[1],
            result.y[0], result.y[1], result.z[0], result.z[1])
        resp = requests.get(cutout_url,
                            headers={'Authorization': 'Token {}'.format(result.token),
                                     'Accept': 'application/blosc'})
        resp.raise_for_status()
        data_decompress = blosc.decompress(resp.content)
        data_np = np.fromstring(data_decompress, dtype=datatype)
        data_direct = np.reshape(data_np, (7, 500, 512))

        data = rmt.cutout(result.x, result.y, result.z, 'uint8', 0)

        assert np.array_equal(data, data_direct)


def collect_input_args(collection, experiment, channel, config_file=None, token=None, url='https://api.boss.neurodata.io', x=None, y=None, z=None, res=0, outdir='./', full_extent=False, print_metadata=False):
    result = argparse.Namespace(
        collection=collection,
        experiment=experiment,
        channel=channel,
        config_file=config_file,
        token=token,
        url=url,
        x=x, y=y, z=z, res=res, outdir=outdir,
        full_extent=full_extent,
        print_metadata=print_metadata
    )
    return result
