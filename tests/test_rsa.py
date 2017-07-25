#!/usr/bin/env python3

from unittest import TestCase

from RSA.rsa import *
from util.inparser import hex_to_ascii, ascii_to_hex

class TestGen(TestCase):
    def test_simple(self):
        r = RSA(61, 53, 17)
        pub, priv = r.gen_keys()
        self.assertEqual(pub.n, 3233)
        self.assertEqual(priv.n, 3233)
        self.assertEqual(priv.d, 413)
        plain_true = ascii_to_hex("H")
        cipher_true = 0xbb8
        cipher = pub.encrypt(plain_true)
        self.assertEqual(cipher_true, cipher)
        self.assertEqual(plain_true, priv.decrypt(cipher))

    def test_error(self):
        with self.assertRaises(RSAError):
            r = RSA(61, 53, 9922)
            r.gen_keys()

# -------------------------------------------------------------------------- #

class TestCTF(TestCase):
    def test_abctf_oldrsa(self):
        plain = "ABCTF{th1s_was_h4rd_in_1980}"
        cipher = 0x41fcc60d2cd6e05c9883c099959de17b1305983c7c99b57b1133a3f507849bd1
        n = 70736025239265239976315088690174594021646654881626421461009089480870633400973
        e = 3
        p = 238324208831434331628131715304428889871
        q = 296805874594538235115008173244022912163
        r = RSA(p, q, e)
        pub, priv = r.gen_keys()
        self.assertEqual(n, pub.n)
        self.assertEqual(n, priv.n)
        self.assertEqual(cipher, pub.encrypt(ascii_to_hex(plain)))
        self.assertEqual(plain, hex_to_ascii(priv.decrypt(cipher)))

    def test_abctf_sexyrsa(self):
        plain = "ABCTF{i_h4ve_an_RSA_fetish_;)}"
        cipher = 293430917376708381243824815247228063605104303548720758108780880727974339086036691092136736806182713047603694090694712685069524383098129303183298249981051498714383399595430658107400768559066065231114145553134453396428041946588586604081230659780431638898871362957635105901091871385165354213544323931410599944377781013715195511539451275610913318909140275602013631077670399937733517949344579963174235423101450272762052806595645694091546721802246723616268373048438591
        p = 1099610570827941329700237866432657027914359798062896153406865588143725813368448278118977438921370935678732434831141304899886705498243884638860011461262640420256594271701812607875254999146529955445651530660964259381322198377196122393
        q = 1099610570827941329700237866432657027914359798062896153406865588143725813368448278118977438921370935678732434831141304899886705498243884638860011461262640420256594271701812607875254999146529955445651530660964259381322198377196122399
        r = RSA(p, q)
        pub, priv = r.gen_keys()
        self.assertEqual(cipher, pub.encrypt(ascii_to_hex(plain)))
        self.assertEqual(plain, hex_to_ascii(priv.decrypt(cipher)))

    def test_icectf_rsa50(self):
        plain = "IceCTF{falls_apart_so_easily_and_reassembled_so_crudely}"
        cipher = 0x4963654354467b66616c6c735f61706172745f736f5f656173696c795f616e645f7265617373656d626c65645f736f5f63727564656c797d
        e = 0x1
        n = 0x180be86dc898a3c3a710e52b31de460f8f350610bf63e6b2203c08fddad44601d96eb454a34dab7684589bc32b19eb27cffff8c07179e349ddb62898ae896f8c681796052ae1598bd41f35491175c9b60ae2260d0d4ebac05b4b6f2677a7609c2fe6194fe7b63841cec632e3a2f55d0cb09df08eacea34394ad473577dea5131552b0b30efac31c59087bfe603d2b13bed7d14967bfd489157aa01b14b4e1bd08d9b92ec0c319aeb8fedd535c56770aac95247d116d59cae2f99c3b51f43093fd39c10f93830c1ece75ee37e5fcdc5b174052eccadcadeda2f1b3a4a87184041d5c1a6a0b2eeaa3c3a1227bc27e130e67ac397b375ffe7c873e9b1c649812edcd
        pub = PubKey(n, e)
        self.assertEqual(cipher, pub.encrypt(ascii_to_hex(plain)))
        priv = PrivKey(n, 0x1)
        self.assertEqual(plain, hex_to_ascii(priv.decrypt(cipher)))

# -------------------------------------------------------------------------- #

class TestWiener(TestCase):
    def test_rm(self):
        e = 0xf70b3bd74801a25eccbde24e01b077677e298391d4197b099a6f961244f04314da7de144dd69a8aa84686bf4ddbd14a6344bbc315218dbbaf29490a44e42e5c4a2a4e76b8101a5ca82351c07b4cfd4e08038c8d5573a827b227bce515b70866724718ec2ac03359614cdf43dd88f1ac7ee453917975a13c019e620e531207692224009c75eaef11e130f8e54cce31e86c84e9366219ae5c250853be145ea87dcf37aa7ece0a994195885e31ebcd8fe742df1cd1370c95b6684ab6c37e84762193c27dd34c3cf3f5e69957b8338f9143a0052c9381d9e2ecb9ef504c954b453f57632705ed44b28a4b5cbe61368e485da6af2dfc901e45868cdd5006913f338a3
        n = 0x0207a7df9d173f5969ad16dc318496b36be39fe581207e6ea318d3bfbe22c8b485600ba9811a78decc6d5aab79a1c2c491eb6d4f39820657b6686391b85474172ae504f48f02f7ee3a2ab31fce1cf9c22f40e919965c7f67a8acbfa11ee4e7e2f3217bc9a054587500424d0806c0e759081651f6e406a9a642de6e8e131cb644a12e46573bd8246dc5e067d2a4f176fef6eec445bfa9db888a35257376e67109faabe39b0cf8afe2ca123da8314d09f2404922fc4116d682a4bdaeecb73f59c49db7fa12a7fc5c981454925c94e0b5472e02d924dad62c260066e07c7d3b1089d5475c2c066b7f94553c75e856e3a2a773c6c24d5ba64055eb8fea3e57b06b04a3
        pub = PubKey(n, e)
        p, q, d = wiener(pub)
        rp = 273067835270880086905225991495379768025497181071655465691068234751894433419924689398578343149876505032891110212422075482294849988417876098468455656340271714411918145829343178315564694346337087829483997746033122936265729805143582391157953230943745740375876718066059315171626227510845447370568918599985468283447
        rq = 240235037993086647490360091251920509660926008787784163933134217892938306866733942789677346753386227305733054945882967240289722901543973488715609201686292184661845932338700104193843036687863902362262743558762135191383008370605906319072352806840967443808455667223189470493469726348267326087313303773058894562037
        d = 5381228493848881413720861860088084031565764565757312238397645291788450924186173990654586679199909846561378831388735501902424890776718740657080660272298531
        self.assertEqual(p, rp)
        self.assertEqual(q, rq)
        self.assertEqual(d, d)

    def test_wiki(self):
        n = 90581
        e = 17993
        p, q, d = wiener(PubKey(n, e))
        self.assertEqual(p, 379)
        self.assertEqual(q, 239)
        self.assertEqual(d, 5)

# -------------------------------------------------------------------------- #

class TestHastad(TestCase):
    def test_rm(self):
        e = 3
        n1 = 0xBED09481E6C5438DEA330688659FB0DDA3B934924B86D522F131D41A4FDD49CA066346BA716D2B2AE6B0AA655EA1C72FC78672532E21B4EA5E268AA321B8A31C5FFAB1A0F7E83BC37892999729D9BA322465237FCB00AC683B16CA9AA40C84496857C6018D8FC7C58F397D0656E8B6C85553F9A14F61965FECE0B85EEEE99B8128BF8B4CFFE25BE78A4B269944320138D45F4A16C84192AB5895FC64A4F2796A87234B48C46F2DF8719F28EFDAD022118652E3D25E44DA3E51FC13344E1C3ABD75E40C624949B29375BAB36E1FF9A692DF39EADCA179F26B4417CD5D71201F7DEEF7BD0533394157EB9CD292602C481448C3C20A36E189D7733B12AC39888F3B
        n2 = 0xBA05F0CCE54B987C3EDADD20FE386AFC91BBA05F6BC9592D5EE3D4FD430D7DC31503F5857A6C75695B46AA93FF792C55C3F7FC814A59B50F01037C7A66BD9A8AB2813B459FC7604F0CBF3E7B4AECA875B6C080685759F84E0956A276A9F789DF9A6CF5D32ED0ED28D05730D068089FBFA2CE6C4DAC9A2B82090A1B84019A3F699E0D26B8E0CD19B90980970D3231BF9BE17C12E970B05F4252D98B78470E75C61B4157489D41CDDA72B2E0EC9F7E310ADFB8BFF29DE344654CBFEE7243280B1F821FE5C90239A850AA4BE43D50C4202352CC97B211D7CB728A142CF2DF7AD73999119D478DFB676A943C5B7CAE30BA0E1A274E23D4CC635504B4B454C717F621
        n3 = 0xABC757E220D1F0DA46D017D0542273FAAEACA99D68EA3B400F99752B5DEBDB67AE3107D8F491F917BA079E14708F702FC8FC1A6189FC1F41EBA334482695642AFC8083D53DDA77B0B58C251926ED779446A137BBC4EFE3572B0D61DFC1A524C2C7891A6DE6BDA5B15B1604284CCA98B97F6E60974CB17F0A5B1A17BEF2007E02FA8A8BF0E0269DE44DAC25C7C7826CBAC2019435373E887658E5FAF733E08AE04A052FA51447FFFB3B9EEDF7FEEC0C8E62AB0E51C516DB537EE93D9F780B20E1665D8E9E541D5E8DE9AA2EA1447B56D07770A2E5B72CAA0891988D97B77F38274830814BD48E338800B0837FEF4135BAD88F5178941406CFDB831FE18171A13F
        pub1 = PubKey(n1, e)
        pub2 = PubKey(n2, e)
        pub3 = PubKey(n3, e)
        c0 = 0xbe35c9bd68acf79b5cdb91bec310b96a00a5089141f6f52c945c95f88e1b4a2c12e129ba93c785eb5122ccaa3885917044e94edc28b7610693ac09be63dfea11b33b6acbf029378f297f9c2d537ad65d31c5f4cbf027685e4444dab49cce9d40cf3985cfcdce1e0b335ff59fee481653833bdfe79f3ef53d16671639ab9a92b749671f01d04ac9e5c616352d1909a9b4365cfea484aa75227a312cf4124eb65256f77a2f08e3514e747b5df26842edd7e975f9952ce4845b8c849e7e62b8c5b4c9dbd6d39e5da1d2dcf5129cbc969f1fd7b7cdff3f4b5fd13915d9a141d69c15c11053a5f22557cfbd067034cfcc887187a8a68b4ca72db57af2a5b6bf0d9745
        c1 = 0x322e0c9e86d569bb75f90ed1ff4688601069791c4f46e47a82486bfd66f0fc3db7cb0bb629b51805a6f65db120b91cfccb3065c5271b1638dbf7c0ee20bc5446814df2534a5492d2dddfc8ac61abd218e871bcf6eee052f7b86c797d12e2777e04be8b527d28eea7bfc82aa4ed8d2d12185cb9232b1a7fe5f4dffa52380ddfc4f2a32bd56ddd541fa04718b763f60e49441280bdc1ae9b299f884d2a4bb20e9ccde63795bc81125a1060e48438a6db53e6d58836191049fb3ec2f00132f83cfa385bd6b83b18db819bfbae370fb2ab98539b2759fc43299efd8d5b7ef0641bec5dbc6a01cf242b9434f5d908e47e8a9bdfb1cdac65140f9723daae78832a7cd3
        c2 = 0x84c41556ca451a1ecdc42a8b7fb0d5b68dcec600cb9fd9fd80e0a33a310e6218bf57067769d16c6c12feccb67160d76428b35608d464b51c299d6ae212c5b5b839d5b762dbc522ef8ef44a6d1fe1cafa58fb45146454bac025908c6cb1532743c50f3c8cd339758e7cff59f1b1dd382379f732df7b4aeab004dd7ee154b74acaad6d1d065350bb38390fa0278655ddcf3641873e06d3ed0cccc3197adcf9778bfb29d08dbf82a4a72aee420d2eded9610bcf485f88e276bf646f2289f61046cfc31d7feb3c5994c847b865c7359283b72a9ee8377e1088e9c214055b7787edf0c88ab45b68f3d7018b28ca94b97850f7988594b38c95387f7292474a43d14dc2
        m = hastad([pub1, pub2, pub3], [c0, c1, c2])
        m_true = 0x427261766f2120506f75722076616c69646572206c65206368616c6c656e67652c206c6120636c656620657374204e6f5370616d57697468525341210a57656c6c20646f6e652c20746865206b657920666f72207468206368616c6c656e6765206973204e6f5370616d57697468525341210a202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020
        self.assertEqual(m, m_true)

# -------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main()
