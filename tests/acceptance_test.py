import io
import subprocess

import pandas
import pytest

seedsAndDomains = {"bedep_dga_0x9be6851a_0xd666e1f3_0x2666ca48_table1_48": ["tzxnmjybkjytxrge.com",
                                                                            "wrovtrqqtperjj.com",
                                                                            "csbenuubveeistri.com",
                                                                            "nxzfpdiecpegwpb4l.com",
                                                                            "pdpilfwaqsr5.com",
                                                                            "wahcabnfsdoqftwd1r.com",
                                                                            "evsnfhkvtwai30.com",
                                                                            "tjqlcsewgnsaeawdj2.com",
                                                                            "bkiyjtzycuhopg.com",
                                                                            "yahgbihifepqb.com",
                                                                            "zmdddkboasql.com",
                                                                            "ijcpgtkkaeryqd.com",
                                                                            "innganvmcvymbwog.com",
                                                                            "hgwtulyiyzm6.com",
                                                                            "xmfskhzszdwxafem2x.com",
                                                                            "dcexrwjvgnzcphs.com",
                                                                            "fqdqoevaqzaq5l.com",
                                                                            "fdqqfsdedxyeuackn5.com",
                                                                            "rchahcisdyaar54.com",
                                                                            "pugpzwvkxwqgs.com",
                                                                            "wmsbscuhjalqvelce.com",
                                                                            "ermxuwiipz8n.com",
                                                                            "vhlidjocyqkzlwjg4.com",
                                                                            "yovrnjtgsmykyf.com",
                                                                            "vraxdeoszjyt5.com",
                                                                            "jlnfxqhwalzt.com",
                                                                            "yuzwsltpdhswnkn.com",
                                                                            "jjjchdeoyoywtuhi.com"],
                   "bedep_dga_0x36a64c8a_0x7cd02d69_0x8cd006d2_table2_48": ["pansmstagppxan.com",
                                                                            "gfxygzqavvbqgqquxu.com",
                                                                            "wrqxmjiipqaccdg.com",
                                                                            "bovxtdkwewxvki.com",
                                                                            "hnfyrpmeewyxliimkp.com",
                                                                            "mojeefeypksck.com",
                                                                            "axrfkkpyqedd2.com",
                                                                            "krjaosssghknpop7e.com",
                                                                            "tqutdqyepxbxvfe.com",
                                                                            "tucnkahbvtidndvll.com",
                                                                            "tmrhkgfybdyeuclu0z.com",
                                                                            "xjayztxvskpxtjx.com",
                                                                            "hbmykijiuaam5.com",
                                                                            "vwyjgnpuhwoylk2j.com",
                                                                            "ebpptpugrkjifmimo6.com",
                                                                            "gliafjovbumvu2.com",
                                                                            "fwptryqcrsbqwkck.com",
                                                                            "qudkebwnpkufjpefc.com",
                                                                            "whsclzbvmvsusyhauk.com",
                                                                            "slwxcjptwaqqpui5p.com",
                                                                            "zdsutwmsjie9.com",
                                                                            "qkcgcvmqgphrs.com"],
                   "bedep_dga_0x4cdff15c_0x1bbae2d4_0xebbac96f_table3_36": ["oungflmaviuh.com",
                                                                            "gvocwssqnxqc6m.com",
                                                                            "vnijkfyhrispjnvzh9.com",
                                                                            "debtpjznzrsplq7.com",
                                                                            "xjhxohepltppnv.com",
                                                                            "pjthfqiljwhzl.com",
                                                                            "tlcujjabwtqadswp5w.com",
                                                                            "ucbmulnexefgqws.com",
                                                                            "cqlgrlyzfbxuhuk.com",
                                                                            "vlrcbvoaxgiyo33.com",
                                                                            "jkoaznelgjmz.com",
                                                                            "ezuelpbwpapz.com",
                                                                            "bqidpkgmbjsqktipst.com",
                                                                            "zkpqcgyzumsjdzoqj.com",
                                                                            "kungbirqasyquomlss.com",
                                                                            "vjtgddeqjxwd.com",
                                                                            "nyowzvycqdquhifut.com",
                                                                            "eaigihezsyeiuif5o.com",
                                                                            "wppitdeosxwp.com",
                                                                            "juakjbdadkeef.com",
                                                                            "qjzjnqlawxrmsssch.com",
                                                                            "ruytjapmstmuaevyzk.com",
                                                                            "sgxrmfuakwwdgj.com",
                                                                            "nvmkraqeinwrq6d.com",
                                                                            "zqknlkfixizerkj6.com",
                                                                            "hzpbeyzhjvuwld9.com",
                                                                            "vdcrpiaofzwjjaoe3l.com",
                                                                            "hzttizvwjnfxlf6i.com"],
                   "bedep_dga_0x52eb3676_0x7952538d_0x89527836_table4_36": ["koocslenjnojra6s.com",
                                                                            "yjhtcarkkwcqjy.com",
                                                                            "keyiiokltxlzv5q.com",
                                                                            "arqduqjglqhzx.com",
                                                                            "fsdccdwliojyx9f.com",
                                                                            "cawevaxdsvwu.com",
                                                                            "uewzytotknoft.com",
                                                                            "livmhlkayepcflsjis.com",
                                                                            "dyuvbpczeiwejh.com",
                                                                            "uyrmmvkhjzouavdzlm.com",
                                                                            "opmytadbbcnvngmke.com",
                                                                            "ejylqzfbintpvhs.com",
                                                                            "chwbubwwfoyerbst8.com",
                                                                            "tlambriqgvzireloy0.com",
                                                                            "dddosmufjueotsa.com",
                                                                            "ulilnrluyycwjs.com",
                                                                            "cpjidiflbjndvspzj.com",
                                                                            "bwwpnadywmr5.com",
                                                                            "eznivbahxnamezo.com",
                                                                            "xwynytrlgzsdnhk.com",
                                                                            "nfvxxjfqurnmgc.com",
                                                                            "hvbgrbcwmysvaw.com",
                                                                            "teqqllqiokvmjzymt.com",
                                                                            "doeowhfqhrljnbh1.com",
                                                                            "hccrjcuumpyf8s.com",
                                                                            "sexpykakihtlx.com",
                                                                            "arkalqtwkzpkac.com",
                                                                            "aetozcdtkkkvxbhac9.com"],
                   "bedep_dga_0x8af8b34d_0x2be8c4b0_0xdbe8ef0b_table5_36": ["cxynbktpncplgxk.com",
                                                                            "rsbgrunupykopwl6l.com",
                                                                            "fyakcomzxeiu.com",
                                                                            "nqbuacdgknokuizs.com",
                                                                            "qvmrzreaplonbz.com",
                                                                            "pungedmvbpwb5i.com",
                                                                            "lhnqldaooggegz.com",
                                                                            "wxpievhychf9.com",
                                                                            "fqyewtrrtudflpha7.com",
                                                                            "zpgkwhvbxbgpqoaun.com",
                                                                            "yvoogcyvffp0b.com",
                                                                            "hmmmljrwko2v.com",
                                                                            "yzcbsibhhxjgylbldp.com",
                                                                            "glyxdxforuaaebxun5.com",
                                                                            "rbrsgzefsd49.com",
                                                                            "jppwzhkguuiac0.com",
                                                                            "flaoxwmnpzisien2.com",
                                                                            "cofifairtehd.com",
                                                                            "zuoxrgpjunruv1g.com",
                                                                            "hsaojspkpkrtf.com",
                                                                            "vnvinqktbkqmgqop2.com",
                                                                            "wdoztkuqqszpmcu7.com",
                                                                            "aoxwpokddpuladggn.com",
                                                                            "labeerhnuyvbs1.com",
                                                                            "uarihgyqjclvyst9h.com",
                                                                            "roovcgytpljife.com",
                                                                            "dqzexlyczqf2q.com",
                                                                            "shdifjuumngp54.com"],
                   "bedep_dga_0xa28eafd8_0x2edfdb46_0xdedff0fd_table6_36": ["nwaslcusqndmdllsa6.com",
                                                                            "bqeglpoirqi0h.com",
                                                                            "jnwebvqzhwrlla7m.com",
                                                                            "mouiwncazbc6.com",
                                                                            "mdupodcvsunn.com",
                                                                            "pmsdktdcijtdrstyr.com",
                                                                            "nhjdssbyymvkolaue5.com",
                                                                            "gxbmjruwurrx.com",
                                                                            "aqnmylzgycqokmyh2h.com",
                                                                            "lpfoxqcdsdotpnr.com",
                                                                            "mpdjmcusvjxchy.com",
                                                                            "qnxiaouwohqfsu59.com",
                                                                            "ebhtccjbriyujaab.com",
                                                                            "kiiggzxeeofium.com",
                                                                            "nskgmfsmacnotha.com",
                                                                            "vgipzlwtwrczqrd.com",
                                                                            "qahelfwyfjqvmjsg1s.com",
                                                                            "vhjnzrkglefskg.com",
                                                                            "phdaicgkreps7n.com",
                                                                            "fsedxzlyswzbedizud.com",
                                                                            "yjhqdluqbjzus.com",
                                                                            "mfiuqkyfwtlsqh4.com"],
                   "bedep_dga_0xda9ce3f7_0xd1cecf92_0x21cee429_table7_36": ["evsvfftykpqhnk.com",
                                                                            "skhsetzruhrrpckyu.com",
                                                                            "fywttqimjc6u.com",
                                                                            "fbgrxexrhjfobv.com",
                                                                            "endgobmokyfsatiq5l.com",
                                                                            "twzhycfitukplgrd.com",
                                                                            "rchmgbyemfyfwchr.com",
                                                                            "mmumigfxwhbr81.com",
                                                                            "dvfospgnlaj9.com",
                                                                            "vlaaoawnxhltr.com",
                                                                            "zkyrrvbdvlzcklnvy.com",
                                                                            "gxwjqafxfgni.com",
                                                                            "gjyllaokuahiyg.com",
                                                                            "nlmljgiujf02.com",
                                                                            "zmzcfwzwdsbqrqup.com",
                                                                            "sxytojwrupu59.com",
                                                                            "hiwdvrausibeuwp7.com",
                                                                            "pwtohreuxomssn.com",
                                                                            "myjwzhqtnryqlcxe.com",
                                                                            "tbgbqvjpfsoqxnb65.com",
                                                                            "yxicmwfvgqxgkgvay.com",
                                                                            "ffbvktelirakdhrvf4.com",
                                                                            "skwcxqzuixeglzwnj.com",
                                                                            "ytjuhvtehhgc.com",
                                                                            "bdeyjmcianqbzfne21.com",
                                                                            "bifsrueyhqwncr.com",
                                                                            "spdsguqkcjwssakd4.com",
                                                                            "kqirfvmhfukpxxtgvu.com"]
                   }


def calculate_bedep_domains(start, end):
    cmd = ["bedep_dga", "--start", start, "--end", end]

    output = subprocess.check_output(cmd, universal_newlines=True)
    df = pandas.read_csv(io.StringIO(output))
    df.set_index("domain", inplace=True)
    return df


class Test_bedep_domains_for_2020_08_06:

    @pytest.fixture(scope="class")
    def bedep_domains_for_2020_08_06(self):
        return calculate_bedep_domains("2020-08-06", "2020-08-06")

    @pytest.mark.parametrize("seed", seedsAndDomains, ids=seedsAndDomains.keys())
    def test_all_domains_are_calculated(self, bedep_domains_for_2020_08_06, seed):
        for domain in seedsAndDomains[seed]:
            data = bedep_domains_for_2020_08_06.loc[domain]
            assert data["seed"] == seed
            assert data["valid_from"] == "2020-08-06T00:00:00"
            assert data["valid_till"] == "2020-08-12T23:59:59"

    def test_validate_amount_of_calculated_domains(self, bedep_domains_for_2020_08_06):
        number_of_seeds = len(bedep_domains_for_2020_08_06["seed"].unique())
        number_of_entries = len(bedep_domains_for_2020_08_06)

        seeds_in_test = len(seedsAndDomains.keys())
        entries_in_test = sum([len(domain_list) for domain_list in seedsAndDomains.values()])

        assert number_of_seeds == seeds_in_test
        assert number_of_entries == entries_in_test

        assert number_of_seeds == 7
        assert number_of_entries == 184


def test_calculate_domains_for_one_month():
    domains = calculate_bedep_domains("2020-01-01", "2020-02-01")
    assert len(domains) == 1026

    assertCompareArray(domains["valid_from"].unique(), ['2019-12-26T00:00:00', '2020-01-02T00:00:00',
                                                        '2020-01-09T00:00:00', '2020-01-16T00:00:00',
                                                        '2020-01-23T00:00:00', '2020-01-30T00:00:00'])
    assertCompareArray(domains["valid_till"].unique(), ['2020-01-01T23:59:59', '2020-01-08T23:59:59',
                                                        '2020-01-15T23:59:59', '2020-01-22T23:59:59',
                                                        '2020-01-29T23:59:59', '2020-02-05T23:59:59'])


@pytest.mark.parametrize("no_currency_date", ['2018-12-26', '2019-01-01'])
def test_check_no_tuesday_data_bug(no_currency_date):
    domains = calculate_bedep_domains(no_currency_date, no_currency_date)

    assert domains["valid_from"].unique() == ['2018-12-20T00:00:00']
    assert domains["valid_till"].unique() == ['2019-01-09T23:59:59']


def assertCompareArray(firstList, secondList):
    assert all([a == b for a, b in zip(sorted(firstList), sorted(secondList))])
