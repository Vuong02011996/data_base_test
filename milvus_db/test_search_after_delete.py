from app.setting import *
import pymongo
from milvus import Milvus, DataType
from pprint import pprint
import numpy as np
from app.milvus_db import milvus_utils as mv
import time

# host = '14.241.120.239'
# port = '11037'


username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")
mongo_client = pymongo.MongoClient("mongodb://%s:%s@%s" % (username, password, host), 11038)


def create_collection_identity_card(collection_test):
    # collection_param_card = {
    #     "fields": [
    #         {
    #             "name": "facial_vector",
    #             "type": DataType.FLOAT_VECTOR,
    #             "params": {"dim": 512}
    #         },
    #     ],
    #     "segment_row_limit": 4096,
    #     "auto_id": True
    # }
    # mv.create_collections(collection_test, collection_param_card)

    db = mongo_client.facial_recognition
    facial_data = db.facial_data.find({"facial_vector": {"$size": 512}})
    facial_vector = []
    vector_add = np.tile(facial_data[11]["facial_vector"], (10000, 1))
    # for t in facial_data[:10]:
    #     facial_vector.append(t["facial_vector"])
    #
    # facial_vector = facial_vector + list(vector_add)
    #
    # print('facial_vector B', facial_vector[0])
    # card_entities = [
    #     {"name": "facial_vector", "values": facial_vector, "type": DataType.FLOAT_VECTOR},
    # ]
    #
    # list_ids_milvus = mv.milvus_client.insert(collection_test, card_entities)
    list_ids_milvus = []
    for i in range(10):
        card_entities = [
            {"name": "facial_vector", "values": list(vector_add), "type": DataType.FLOAT_VECTOR},
        ]
        list_ids_milvus = mv.milvus_client.insert(collection_test, card_entities)

    mv.milvus_client.flush([collection_test])
    return list_ids_milvus


def delete_ids_milvus(collection_name, list_ids):
    print('entity before delete:', mv.milvus_client.count_entities(collection_name))
    status = mv.milvus_client.delete_entity_by_id(collection_name, list_ids)
    print('status delete', status)
    print('entity after delete:', mv.milvus_client.count_entities(collection_name))
    mv.milvus_client.compact(collection_name)
    mv.milvus_client.flush([collection_name], timeout=1000)
    # time.sleep(5)
    print('entity after delete:', mv.milvus_client.count_entities(collection_name))


def get_entity_by_ids(collection_name, list_ids):
    return mv.milvus_client.get_entity_by_id(collection_name, list_ids, fields=['body_vector'])


def search_identity_card(collection_name):
    db = mongo_client.facial_recognition
    facial_data = db.facial_data.find({"facial_vector": {"$size": 512}})
    facial_vector = []

    for t in facial_data[2:3]:
        facial_vector.append(t["facial_vector"])
        break

    # facial_vector_test = [0.05700881779193878, -0.07108140736818314, -0.0034515687730163336, 0.04408949241042137, 0.03530711308121681, 0.06208732724189758, 0.0616501122713089, -0.022576576098799706, -0.01331719197332859, -0.07904601097106934, 0.019241349771618843, -0.0014881741954013705, 0.07418721914291382, 0.03215247765183449, -0.01723584160208702, -0.005599396303296089, -0.06377788633108139, 0.030009616166353226, -0.030147384852170944, -0.0720498189330101, 0.030202284455299377, 0.03174230828881264, -0.024573491886258125, 0.0294832494109869, -0.03932282328605652, 6.246391421882436e-05, 0.02611722983419895, 0.06340557336807251, 0.009321554563939571, -0.047702837735414505, -0.09291882067918777, -0.0027074492536485195, 0.0746031329035759, 0.023117203265428543, -0.05091879889369011, 0.038143008947372437, 0.02819697931408882, 0.06953679770231247, -0.04425021633505821, 0.029205797240138054, -0.03980063647031784, 0.04452447220683098, -0.036784492433071136, 0.04739778861403465, -0.0477190762758255, 0.017004745081067085, -0.03152507543563843, -0.013814905658364296, 0.02056766301393509, -0.022552525624632835, -0.017298094928264618, 0.014831704087555408, -0.008739661425352097, -0.037748031318187714, -0.0014457327779382467, -0.02572568692266941, -0.05410977080464363, -0.04448455199599266, -0.030592096969485283, -0.057988543063402176, -0.003385357791557908, 0.027225283905863762, -0.03847355768084526, -0.005682375282049179, 0.0179174542427063, 0.009231870993971825, -0.008960027247667313, 0.04167879372835159, -0.04862457141280174, -0.00738219590857625, 0.06887897849082947, -0.01936786063015461, 0.06415031850337982, -0.08039137721061707, 0.0027358278166502714, 0.02173008769750595, 0.004263212438672781, 0.07129282504320145, -0.061721183359622955, 0.025521624833345413, 0.037258733063936234, -0.04388832673430443, 0.06490658223628998, -0.021690599620342255, 0.049742233008146286, -0.0515948086977005, -0.08246774971485138, 0.01948973722755909, -0.06528549641370773, 0.0013627303997054696, 0.011105875484645367, 0.018110668286681175, -0.03431889787316322, -0.049778543412685394, 0.038259729743003845, 0.0031574165914207697, -0.0184010062366724, -0.051327601075172424, -0.010219837538897991, -0.036220893263816833, -0.04365324601531029, -0.053388163447380066, 0.05852839723229408, 0.013255656696856022, -0.028567638248205185, -0.034690577536821365, -0.027070295065641403, 0.031016824766993523, 0.044339779764413834, -0.07340910285711288, 0.049983080476522446, -0.05598857253789902, -0.0165218785405159, -0.05332003906369209, 0.03324733301997185, 0.019974160939455032, -0.007158714346587658, 0.06853211671113968, 0.005483114160597324, -0.0029785563237965107, 0.022487152367830276, -0.00023427869018632919, 0.021695414558053017, 0.028570236638188362, 0.009864798747003078, -0.030057210475206375, -0.02874058485031128, -0.009063742123544216, 0.01763620600104332, 0.01704251579940319, -0.007820595987141132, 0.06477006524801254, 0.057466842234134674, 0.03789237514138222, -0.03750988841056824, -0.03705627843737602, -0.10061559081077576, -0.04415886104106903, 0.022481508553028107, 0.03706183284521103, 0.02489432692527771, -0.03925548866391182, 0.02568354457616806, 0.09037207067012787, -0.02720300294458866, -0.011234750039875507, 0.018401140347123146, -0.06442967057228088, -0.009431954473257065, 0.052238963544368744, 0.1176152303814888, 0.03184325993061066, 0.0020199010614305735, 0.03335461765527725, -0.009079004637897015, 0.019719691947102547, -0.033599402755498886, 0.04064200818538666, 0.008624212816357613, 0.017718197777867317, -0.08411569893360138, -0.03537726402282715, 0.08214026689529419, -0.027837947010993958, -0.1365961879491806, 0.0033254483714699745, -0.0026803952641785145, 0.033726297318935394, 0.04619340971112251, -0.013500172644853592, -0.04073358699679375, 0.009320789948105812, -0.0988938957452774, -0.039650022983551025, 0.041672609746456146, -0.04129062965512276, -0.005504278931766748, 0.052193090319633484, -0.07335606962442398, -0.018461555242538452, 0.06933856755495071, 0.04728486388921738, 0.034324806183576584, 0.0498187430202961, -0.00435633072629571, -0.008227786980569363, 0.08054474741220474, 0.00013573784963227808, -0.008376719430088997, -0.007710886653512716, -0.07087597250938416, 0.009707033634185791, -0.009661685675382614, -0.01378869079053402, -0.031713567674160004, -0.021153589710593224, 0.01003243774175644, -0.058298200368881226, 0.04579140618443489, -0.09285705536603928, -0.017330845817923546, -0.04281770810484886, 0.057495761662721634, 0.013348784297704697, 0.02984066680073738, 0.076840840280056, 0.021019965410232544, 0.10899943113327026, 0.02665541134774685, -0.011008284986019135, -0.003708329750224948, -0.01675533503293991, -0.04060114175081253, 0.06937942653894424, 0.05662604421377182, -0.12964369356632233, -0.035757601261138916, -0.009733709506690502, 0.002004370093345642, 0.06370163708925247, -0.004641309380531311, 0.06363794952630997, 0.01550560723990202, -0.016356630250811577, -0.033179137855768204, 0.02478482574224472, 0.0077752345241606236, 0.051446929574012756, -0.005216782912611961, 0.0712580606341362, -0.10297389328479767, -0.09917418658733368, 0.06072550639510155, -0.04529491439461708, 0.07281886786222458, -0.0308426171541214, -0.08163132518529892, 0.005813175812363625, 0.043850068002939224, -0.025111757218837738, 0.009867122396826744, 0.03523018956184387, -0.04176584631204605, 0.07947716861963272, -0.015996543690562248, -0.05602692440152168, -0.05318313091993332, 0.008747420273721218, 0.00029599718982353806, 0.051067180931568146, -0.12705348432064056, -0.06399194896221161, 0.051004018634557724, -0.016281738877296448, 0.050078049302101135, -0.06414502114057541, 0.012325002811849117, -0.11917779594659805, 0.005819653160870075, 0.02188420668244362, -0.0020657803397625685, -0.04033572971820831, 0.01727793738245964, 0.0004803288320545107, 0.038706764578819275, -0.016743971034884453, 0.020428527146577835, 0.016881601884961128, -0.06705307960510254, 0.04328904673457146, -0.018263954669237137, 0.019715508446097374, 0.045451920479536057, 0.013878382742404938, -0.02443251572549343, -0.07491001486778259, 0.06658648699522018, 0.05361734703183174, -0.021097427234053612, -0.027136782184243202, 0.04664634168148041, 0.020999250933527946, -0.03193153068423271, 0.023758020251989365, 0.05187197029590607, -0.04640978202223778, 0.01015492808073759, 0.046674322336912155, -0.04105162248015404, -0.038924526423215866, -0.034265536814928055, 0.012539388611912727, -0.03924679011106491, -0.024817679077386856, -0.0278051495552063, -0.012243498116731644, -0.03202058747410774, -0.009485652670264244, -0.02870226837694645, -0.08965211361646652, 0.0009653239394538105, -0.01010270044207573, -0.013143271207809448, -0.007341173477470875, -0.015894833952188492, -0.012958117760717869, 0.07270979881286621, 0.05393349751830101, -0.016355380415916443, 0.03161017224192619, 0.03172881901264191, 0.028982503339648247, -0.0011352094588801265, 0.10093072801828384, -0.028940729796886444, -0.041353870183229446, -0.03687826916575432, -0.040660761296749115, 0.007716810796409845, 0.016771549358963966, -0.0695691853761673, 0.01178377028554678, -0.006316314917057753, -0.06341449916362762, 0.025396505370736122, 0.035411544144153595, -0.08181178569793701, 0.02076876349747181, -0.062068872153759, -0.0505460724234581, -0.02159600518643856, 0.0482679046690464, 0.08084044605493546, 0.029032880440354347, -0.0138667868450284, 0.061957791447639465, -0.038999248296022415, -0.032193977385759354, -0.029474055394530296, -0.07832968980073929, -0.01038538757711649, -0.004680948331952095, -0.030594168230891228, 0.050176020711660385, -0.017185470089316368, -0.031133286654949188, -0.08092007040977478, 0.014131644740700722, 0.049534570425748825, -0.06747733056545258, 0.06419253349304199, 0.020028531551361084, -0.037753112614154816, -0.02705063670873642, 0.025915231555700302, 0.03303135558962822, 0.024449894204735756, 0.014542336575686932, 0.04097630828619003, -0.016256099566817284, -0.022730663418769836, 0.012227430008351803, -0.05465295538306236, -0.07589689642190933, 0.05755716934800148, 0.033778272569179535, 0.04085303470492363, 0.05288852006196976, -0.09057775884866714, 0.054557446390390396, -0.08605946600437164, 0.07287256419658661, 0.023620352149009705, 0.0449773333966732, -0.06294575333595276, 0.020812150090932846, -0.010897249914705753, 0.04273190721869469, 0.0380224771797657, 0.021022813394665718, -0.052431464195251465, -0.020311176776885986, -0.06971205770969391, -0.0130881043151021, 0.01351187750697136, -0.02035469375550747, 0.05674906075000763, 0.030972950160503387, -0.008502855896949768, 0.013382616452872753, -0.038281284272670746, 0.02236178144812584, 0.050233639776706696, 0.011221199296414852, -0.07243988662958145, 0.0347871333360672, -0.031559187918901443, -0.021953746676445007, -0.04297948256134987, 0.08377643674612045, 0.0334111750125885, -0.02183256670832634, 0.06561663001775742, -0.006182623095810413, -0.03629208728671074, -0.06312102824449539, 0.044968344271183014, -0.01281580701470375, 0.0007488180999644101, -0.00513992877677083, -0.07876080274581909, 0.04677257314324379, -0.03481133654713631, 0.01544679794460535, 0.05849051848053932, -0.038641367107629776, -3.839530472760089e-05, -0.02892279624938965, 0.023630665615200996, -0.00886545330286026, -0.054936278611421585, -0.019833922386169434, 0.015350396744906902, 0.003964687697589397, 0.016429858282208443, -0.0016178018413484097, 0.02323755994439125, 0.05087070167064667, 0.06758452206850052, 0.02955974079668522, 0.0010134170297533274, -0.054305948317050934, 0.018708961084485054, 0.0195001307874918, 0.02080162987112999, 0.016714803874492645, 0.000508311262819916, -0.0286079254001379, 0.038593944162130356, 0.046854306012392044, 0.053808316588401794, -0.002465739380568266, -0.06759514659643173, -0.002012672135606408, 0.02741100639104843, -0.02637758105993271, 0.01983252726495266, 0.008086287416517735, 0.016120711341500282, 0.0009332944173365831, 0.06439987570047379, -0.06730470061302185, -0.05572385713458061, -0.022941770032048225, 0.0837969034910202, -0.0596185065805912, 0.025274144485592842, 0.003705536015331745, -0.05238615721464157, -0.026468655094504356, 0.023377038538455963, 0.08066993951797485, 0.08364962786436081, 0.007519283797591925, -0.017035558819770813, 0.03121781162917614, -0.06528699398040771, 0.06582425534725189, 0.04491356015205383, 0.03562328591942787, -0.015713989734649658, 0.02171744592487812, -0.07338780164718628, -0.0024766838178038597, -0.02491900324821472, 0.016941869631409645, -0.03988879919052124, 0.010249059647321701, -0.07055245339870453, 0.04199424758553505, 0.00041436354513280094, -0.02871701493859291, 0.011076712049543858, -0.010551798157393932, 0.017779866233468056, -0.007120140362530947, 0.007088000420480967, -0.06742248684167862, -0.017386483028531075, 0.011220313608646393, 0.03965555876493454, -0.10345693677663803, 0.032828692346811295, -0.045667652040719986, 0.02860373444855213, 0.10634130239486694, -0.024298183619976044, 0.08309551328420639, -0.04164484888315201, -0.009163805283606052, 0.010647349990904331, -0.002631568582728505, 0.03636471927165985, 0.009583095088601112, -0.08845619112253189, -0.04618417099118233, 0.020054984837770462, 0.017806168645620346, 0.003844180144369602, 0.02996940352022648, -0.07485976815223694, 0.022764146327972412]
    # facial_vector.append(facial_vector_test)
    print(len(facial_vector), len(facial_vector[0]))
    print('vector search A: ', facial_vector[0])

    dsl = {
        "bool": {
            "must": [
                {
                    "vector": {
                        "facial_vector": {"topk": 2, "query": facial_vector, "metric_type": "L2"}
                    }

                }
            ]
        }
    }

    results = mv.milvus_client.search(collection_name, dsl, fields=['facial_vector'])
    print("\n----------search----------")
    list_ids_delete = []
    for entities in results:
        for top_dis in entities:
            print("- id: {}".format(top_dis.id))
            list_ids_delete.append((top_dis.id))
            print("- distance: {}".format(top_dis.distance))
            current_entity = top_dis.entity
            # print("- facial_vector: {}".format(current_entity.facial_vector))
    return list_ids_delete


def search_body(collection_test, body_vector, object_uuid, top_k=1):

    term_query = {
        "term": {
            # "process_uuid": [11],
            "object_uuid": [object_uuid]
        }
    }

    vector_query = {
                    "vector": {
                        "body_vector": {"topk": top_k, "query": body_vector, "metric_type": "L2"}
                    }

                }

    dsl = {
        "bool": {
            "must": [term_query, vector_query]
        }
    }
    results = mv.milvus_client.search(collection_test, dsl, fields=['body_vector'])
    print("\n----------search----------")
    list_ids_delete = []
    for entities in results:
        for top_dis in entities:
            print("- id: {}".format(top_dis.id))
            list_ids_delete.append(top_dis.id)
            print("- distance: {}".format(top_dis.distance))
            current_entity = top_dis.entity
            # print("- body_vector: {}".format(current_entity.body_vector))

    return list_ids_delete


def search_after_delete(list_ids_delete, body_vector, object_uuid):
    # time.sleep(10)
    print('vector search A: ', body_vector[0])
    term_query = {
        "term": {
            # "process_uuid": [11],
            "object_uuid": [object_uuid]
        }
    }
    body_vector[0][0] = 1
    vector_query = {
        "vector": {
            "body_vector": {"topk": 2, "query": body_vector, "metric_type": "L2"}
        }

    }

    dsl1 = {
        "bool": {
            "must": [term_query, vector_query]
        }
    }
    results_2 = mv.milvus_client.search(collection_test, dsl1, fields=['body_vector'])
    print("\n----------search----------")
    for entities in results_2:
        for top_dis in entities:
            print("- id: {}".format(top_dis.id))
            print("- distance: {}".format(top_dis.distance))
            current_entity = top_dis.entity
            print("- body_vector: {}".format(current_entity.body_vector))


def delete(collection_test, list_ids_delete):
    delete_ids_milvus(collection_test, list_ids_delete)


def test():
    collection_test = 'card'
    # list_ids_milvus = create_collection_identity_card(collection_test)
    # print('list_ids_milvus', list_ids_milvus)
    # list_ids = [list_ids_milvus[0]]
    # list_ids = [1610950703270755000]
    list_ids_delete = search_identity_card(collection_test)
    print('list_ids_delete', list_ids_delete)
    delete_ids_milvus(collection_test, list_ids_delete)
    # result_get = get_entity_by_ids(collection_test, list_ids)
    search_identity_card(collection_test)
    # search_identity_card(collection_test)
    # test_get_entities_by_ids(collection_test)


if __name__ == '__main__':
    test()
    # collection_test = 'bodies'
    #
    # body_vector = []
    # list_ids = [1610702159781844000]
    # object_uuid = 1610702133736000
    # result_get = get_entity_by_ids(collection_test, list_ids)
    #
    # for entity in result_get:
    #     if entity is not None:
    #         body_vector.append(entity.get('body_vector'))
    # print('vector search A: ', body_vector[0])
    # list_ids_delete = search_body(collection_test, body_vector, object_uuid)
    # print('list_ids_delete', list_ids_delete)
    # delete(collection_test, list_ids_delete)
    # list_ids_delete = search_body(collection_test, body_vector, object_uuid, top_k=2)
