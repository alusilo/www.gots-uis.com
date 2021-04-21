import numpy as np

class GlassMaterial(object):
	"""docstring for GlassMaterial"""
	def __init__(self, **kwargs):
		super(GlassMaterial, self).__init__()
		self.type = kwargs.get('material', 'N-BK7')
		
	def disperssion_formula(self,wl):
		refractive_index = None
		# if self.type == 'N-X':
		# 	if wl == 0.4861: refractive_index = 1.85522180093592
		# 	if wl == 0.5876: refractive_index = 1.8502442055719617
		# 	if wl == 0.6563: refractive_index = 1.84805763676
		# if self.type == 'N-Y':
		# 	if wl == 0.4861: refractive_index = 1.85522180093592
		# 	if wl == 0.5876: refractive_index = 1.8502442055719617
		# 	if wl == 0.6563: refractive_index = 1.85005763676
		if self.type == 'N-X':
			refractive_index = 0.1*wl + 1.4
		if self.type == 'N-Y':
			refractive_index = 0.1*wl + 1.8
		if self.type == 'X1':
			refractive_index = 1.376
		if self.type == 'X2':
			refractive_index = 1.336
		if self.type == 'X3':
			refractive_index = 1.406#1.386
		if self.type == 'X4':
			refractive_index = 1.337
		##### SCHOTT Glasses #####
		##### FK #####
		if self.type == 'N-FK51A':
			refractive_index = np.sqrt(1 + 0.97124782*wl**2/(wl**2-0.00472301995) + 0.216901417*wl**2/(wl**2-0.0153575612) + 0.904651666*wl**2/(wl**2-168.6813300))
		if self.type == 'N-FK58':
			refractive_index = np.sqrt(1 + 0.73804271*wl**2/(wl**2-0.00339065607) + 0.363371967*wl**2/(wl**2-0.0117551189) + 0.989296264*wl**2/(wl**2-212.8421450))
		if self.type == 'N-FK5':
			refractive_index = np.sqrt(1 + 0.84430934*wl**2/(wl**2-0.00475111955) + 0.344147824*wl**2/(wl**2-0.0149814849) + 0.910790213*wl**2/(wl**2-97.8600293))
		##### PK #####
		if self.type == 'N-PK51':
			refractive_index = np.sqrt(1 + 1.15610775*wl**2/(wl**2-0.00585597402) + 0.153229344*wl**2/(wl**2-0.0194072416) + 0.785618966*wl**2/(wl**2-140.5370460))
		if self.type == 'N-PK52A':
			refractive_index = np.sqrt(1 + 1.02960700*wl**2/(wl**2-0.00516800155) + 0.188050600*wl**2/(wl**2-0.0166658798) + 0.736488165*wl**2/(wl**2-138.9641290))
		##### BK #####
		if self.type == 'N-BK10':
			refractive_index = np.sqrt(1 + 0.88830813*wl**2/(wl**2-0.00516900822) + 0.328964475*wl**2/(wl**2-0.0161190045) + 0.984610769*wl**2/(wl**2-99.7575331))
		if self.type == 'N-BK7':
			refractive_index = np.sqrt(1 + 1.03961212*wl**2/(wl**2-0.00600069867) + 0.231792344*wl**2/(wl**2-0.0200179144) + 1.010469450*wl**2/(wl**2-103.5606530))
		##### PSK #####
		if self.type == 'N-PSK3':
			refractive_index = np.sqrt(1 + 0.88727211*wl**2/(wl**2-0.00469824067) + 0.489592425*wl**2/(wl**2-0.0161818463) + 1.048652960*wl**2/(wl**2-104.3749750))
		if self.type == 'N-PSK53A':
			refractive_index = np.sqrt(1 + 1.38121836*wl**2/(wl**2-0.00706416337) + 0.196745645*wl**2/(wl**2-0.0233251345) + 0.886089205*wl**2/(wl**2-97.4847345))
		##### K #####
		if self.type == 'N-ZK7':
			refractive_index = np.sqrt(1 + 1.07715032*wl**2/(wl**2-0.00676601657) + 0.168079109*wl**2/(wl**2-0.0230642817) + 0.851889892*wl**2/(wl**2-89.0498778))
		if self.type == 'N-ZK7A':
			refractive_index = np.sqrt(1 + 1.07509891*wl**2/(wl**2-0.00676601657) + 0.168895044*wl**2/(wl**2-0.0230642817) + 0.860503983*wl**2/(wl**2-89.0498778))
		if self.type == 'N-K7':
			refractive_index = np.sqrt(1 + 1.12735550*wl**2/(wl**2-0.00720341707) + 0.124412303*wl**2/(wl**2-0.0269835916) + 0.827100531*wl**2/(wl**2-100.3845880))
		if self.type == 'N-K5':
			refractive_index = np.sqrt(1 + 1.08511833*wl**2/(wl**2-0.00661099503) + 0.199562005*wl**2/(wl**2-0.0241108660) + 0.930511663*wl**2/(wl**2-111.9827770))
		if self.type == 'N-K10':
			refractive_index = np.sqrt(1 + 1.15687082*wl**2/(wl**2-0.00809424251) + 0.064262544*wl**2/(wl**2-0.0386051284) + 0.872376139*wl**2/(wl**2-104.7477300))
		##### KF #####
		if self.type == 'N-KF9':
			refractive_index = np.sqrt(1 + 1.19286778*wl**2/(wl**2-0.00839154696) + 0.089334657*wl**2/(wl**2-0.0404010786) + 0.920819805*wl**2/(wl**2-112.5724460))
		##### BAK #####
		if self.type == 'N-BAK2':
			refractive_index = np.sqrt(1 + 1.01662154*wl**2/(wl**2-0.00592383763) + 0.319903051*wl**2/(wl**2-0.0203828415) + 0.937232995*wl**2/(wl**2-113.1184170))
		if self.type == 'N-BAK1':
			refractive_index = np.sqrt(1 + 1.12365662*wl**2/(wl**2-0.00644742752) + 0.309276848*wl**2/(wl**2-0.0222284402) + 0.881511957*wl**2/(wl**2-107.2977510))
		if self.type == 'N-BAK4':
			refractive_index = np.sqrt(1 + 1.28834642*wl**2/(wl**2-0.00779980626) + 0.132817724*wl**2/(wl**2-0.0315631177) + 0.945395373*wl**2/(wl**2-105.9658750))
		##### BALF #####
		if self.type == 'N-BALF5':
			refractive_index = np.sqrt(1 + 1.28385965*wl**2/(wl**2-0.00825815975) + 0.071930094*wl**2/(wl**2-0.0441920027) + 1.050489270*wl**2/(wl**2-107.0973240))
		if self.type == 'N-KZFS2':
			refractive_index = np.sqrt(1 + 1.23697554*wl**2/(wl**2-0.00747170505) + 0.153569376*wl**2/(wl**2-0.0308053556) + 0.903976272*wl**2/(wl**2-70.1731084))
		if self.type == 'N-BALF4':
			refractive_index = np.sqrt(1 + 1.31004128*wl**2/(wl**2-0.00796596450) + 0.142038259*wl**2/(wl**2-0.0330672072) + 0.964929351*wl**2/(wl**2-109.1973200))
		##### SK #####
		if self.type == 'N-SK11':
			refractive_index = np.sqrt(1 + 1.17963631*wl**2/(wl**2-0.00680282081) + 0.229817295*wl**2/(wl**2-0.0219737205) + 0.935789652*wl**2/(wl**2-101.5132320))
		if self.type == 'N-SK5':
			refractive_index = np.sqrt(1 + 0.99146382*wl**2/(wl**2-0.00522730467) + 0.495982121*wl**2/(wl**2-0.0172733646) + 0.987393925*wl**2/(wl**2-98.3594579))
		if self.type == 'N-SK14':
			refractive_index = np.sqrt(1 + 0.93615537*wl**2/(wl**2-0.00461716525) + 0.594052018*wl**2/(wl**2-0.0168859270) + 1.043745830*wl**2/(wl**2-103.7362650))
		if self.type == 'N-SK16':
			refractive_index = np.sqrt(1 + 1.34317774*wl**2/(wl**2-0.00704687339) + 0.241144399*wl**2/(wl**2-0.0229005000) + 0.994317969*wl**2/(wl**2-92.7508526))
		if self.type == 'N-SK4':
			refractive_index = np.sqrt(1 + 1.32993741*wl**2/(wl**2-0.00716874107) + 0.228542996*wl**2/(wl**2-0.0246455892) + 0.988465211*wl**2/(wl**2-100.8863640))
		if self.type == 'N-SK2':
			refractive_index = np.sqrt(1 + 1.28189012*wl**2/(wl**2-0.00727191640) + 0.257738258*wl**2/(wl**2-0.0242823527) + 0.968186040*wl**2/(wl**2-110.3777730))
		##### SSK #####
		if self.type == 'N-SSK2':
			refractive_index = np.sqrt(1 + 1.43060270*wl**2/(wl**2-0.00823982975) + 0.153150554*wl**2/(wl**2-0.0333736841) + 1.013909040*wl**2/(wl**2-106.8708220))
		if self.type == 'N-SSK5':
			refractive_index = np.sqrt(1 + 1.59222659*wl**2/(wl**2-0.00920284626) + 0.103520774*wl**2/(wl**2-0.0423530072) + 1.051740160*wl**2/(wl**2-106.9273740))
		if self.type == 'N-SSK8':
			refractive_index = np.sqrt(1 + 1.44857867*wl**2/(wl**2-0.00869310149) + 0.117965926*wl**2/(wl**2-0.0421566593) + 1.069375280*wl**2/(wl**2-111.3006660))
		##### LK #####
		if self.type == 'N-LAK21':
			refractive_index = np.sqrt(1 + 1.22718116*wl**2/(wl**2-0.00602075682) + 0.420783743*wl**2/(wl**2-0.0196862889) + 1.012848430*wl**2/(wl**2-88.4370099))
		if self.type == 'N-LAK7':
			refractive_index = np.sqrt(1 + 1.23679889*wl**2/(wl**2-0.00610105538) + 0.445051837*wl**2/(wl**2-0.0201388334) + 1.017458880*wl**2/(wl**2-90.6380380))
		if self.type == 'N-LAK22':
			refractive_index = np.sqrt(1 + 1.14229781*wl**2/(wl**2-0.00585778594) + 0.535138441*wl**2/(wl**2-0.0198546147) + 1.040883850*wl**2/(wl**2-100.8340170))
		if self.type == 'N-LAK12':
			refractive_index = np.sqrt(1 + 1.17365704*wl**2/(wl**2-0.00577031797) + 0.588992398*wl**2/(wl**2-0.0200401678) + 0.978014394*wl**2/(wl**2-95.4873482))
		if self.type == 'N-LAK14':
			refractive_index = np.sqrt(1 + 1.50781212*wl**2/(wl**2-0.00746098727) + 0.318866829*wl**2/(wl**2-0.0242024834) + 1.142872130*wl**2/(wl**2-80.9565165))
		if self.type == 'N-LAK9':
			refractive_index = np.sqrt(1 + 1.46231905*wl**2/(wl**2-0.00724270156) + 0.344399589*wl**2/(wl**2-0.0243353131) + 1.155083720*wl**2/(wl**2-85.4686868))
		if self.type == 'N-LAK35':
			refractive_index = np.sqrt(1 + 1.39324260*wl**2/(wl**2-0.00715959695) + 0.418882766*wl**2/(wl**2-0.0233637446) + 1.043807000*wl**2/(wl**2-88.3284426))
		if self.type == 'N-LAK34':
			refractive_index = np.sqrt(1 + 1.26661442*wl**2/(wl**2-0.00589278062) + 0.665919318*wl**2/(wl**2-0.0197509041) + 1.124961200*wl**2/(wl**2-78.8894174))
		if self.type == 'N-LAK8':
			refractive_index = np.sqrt(1 + 1.33183167*wl**2/(wl**2-0.00620023871) + 0.546623206*wl**2/(wl**2-0.0216465439) + 1.190840150*wl**2/(wl**2-82.5827736))
		if self.type == 'N-LAK10':
			refractive_index = np.sqrt(1 + 1.72878017*wl**2/(wl**2-0.00886014635) + 0.169257825*wl**2/(wl**2-0.0363416509) + 1.193869560*wl**2/(wl**2-82.9009069))
		if self.type == 'N-LAK33B':
			refractive_index = np.sqrt(1 + 1.42288601*wl**2/(wl**2-0.00670283452) + 0.593661336*wl**2/(wl**2-0.0219416210) + 1.161352600*wl**2/(wl**2-80.7407701))
		##### F #####
		if self.type == 'N-F2':
			refractive_index = np.sqrt(1 + 1.39757037*wl**2/(wl**2-0.00995906143) + 0.159201403*wl**2/(wl**2-0.0546931752) + 1.268654300*wl**2/(wl**2-119.2483460))
		##### SF #####
		if self.type == 'N-SF2':
			refractive_index = np.sqrt(1 + 1.47343127*wl**2/(wl**2-0.01090190980) + 0.163681849*wl**2/(wl**2-0.0585683687) + 1.369208990*wl**2/(wl**2-127.4049330))
		if self.type == 'N-SF5':
			refractive_index = np.sqrt(1 + 1.52481889*wl**2/(wl**2-0.011254756) + 0.187085527*wl**2/(wl**2-0.0588995392) + 1.42729015*wl**2/(wl**2-129.141675))
		if self.type == 'N-SF8':
			refractive_index = np.sqrt(1 + 1.55075812*wl**2/(wl**2-0.01143383440) + 0.209816918*wl**2/(wl**2-0.0582725652) + 1.462054910*wl**2/(wl**2-133.2416500))
		if self.type == 'N-SF15':
			refractive_index = np.sqrt(1 + 1.57055634*wl**2/(wl**2-0.01165070140) + 0.218987094*wl**2/(wl**2-0.0597856897) + 1.508240170*wl**2/(wl**2-132.7093390))
		if self.type == 'N-SF1':
			refractive_index = np.sqrt(1 + 1.60865158*wl**2/(wl**2-0.01196548790) + 0.237725916*wl**2/(wl**2-0.0590589722) + 1.515306530*wl**2/(wl**2-135.5216760))
		if self.type == 'N-SF10':
			refractive_index = np.sqrt(1 + 1.62153902*wl**2/(wl**2-0.0122241457) + 0.256287842*wl**2/(wl**2-0.0595736775) + 1.64447552*wl**2/(wl**2-147.468793))
		if self.type == 'N-SF4':
			refractive_index = np.sqrt(1 + 1.67780282*wl**2/(wl**2-0.01267934500) + 0.282849893*wl**2/(wl**2-0.0602038419) + 1.635392760*wl**2/(wl**2-145.7604960))
		if self.type == 'N-SF14':
			refractive_index = np.sqrt(1 + 1.69022361*wl**2/(wl**2-0.01305121130) + 0.288870052*wl**2/(wl**2-0.0613691880) + 1.704518700*wl**2/(wl**2-149.5176890))
		if self.type == 'N-SF11':
			refractive_index = np.sqrt(1 + 1.73759695*wl**2/(wl**2-0.013188707) + 0.313747346*wl**2/(wl**2-0.0623068142) + 1.89878101*wl**2/(wl**2-155.23629))
		if self.type == 'N-SF6':
			refractive_index = np.sqrt(1 + 1.77931763*wl**2/(wl**2-0.01337141820) + 0.338149866*wl**2/(wl**2-0.0617533621) + 2.087344740*wl**2/(wl**2-174.0175900))
		if self.type == 'N-SF57':
			refractive_index = np.sqrt(1 + 1.87543831*wl**2/(wl**2-0.01417495180) + 0.373757490*wl**2/(wl**2-0.0640509927) + 2.300017970*wl**2/(wl**2-177.3897950))
		if self.type == 'N-SF66':
			refractive_index = np.sqrt(1 + 2.02459760*wl**2/(wl**2-0.01470532250) + 0.470187196*wl**2/(wl**2-0.0692998276) + 2.599704330*wl**2/(wl**2-161.8176010))
		##### BAF #####
		if self.type == 'N-BAF10':
			refractive_index = np.sqrt(1 + 1.58514950*wl**2/(wl**2-0.00926681282) + 0.143559385*wl**2/(wl**2-0.0424489805) + 1.08521269*wl**2/(wl**2-105.613573))
		if self.type == 'N-BAF52':
			refractive_index = np.sqrt(1 + 1.43903433*wl**2/(wl**2-0.00907800128) + 0.096704605*wl**2/(wl**2-0.0508212080) + 1.098758180*wl**2/(wl**2-105.6918560))
		if self.type == 'N-KZFS4':
			refractive_index = np.sqrt(1 + 1.35055424*wl**2/(wl**2-0.00876282070) + 0.197575506*wl**2/(wl**2-0.0371767201) + 1.099629920*wl**2/(wl**2-90.3866994))
		if self.type == 'N-BAF4':
			refractive_index = np.sqrt(1 + 1.42056328*wl**2/(wl**2-0.00942015382) + 0.102721269*wl**2/(wl**2-0.0531087291) + 1.143809760*wl**2/(wl**2-110.2788560))
		if self.type == 'N-BAF51':
			refractive_index = np.sqrt(1 + 1.51503623*wl**2/(wl**2-0.00942734715) + 0.153621958*wl**2/(wl**2-0.0430826500) + 1.154279090*wl**2/(wl**2-124.8898680))
		##### BASF #####
		if self.type == 'N-KZFS11':
			refractive_index = np.sqrt(1 + 1.33222450*wl**2/(wl**2-0.00840298480) + 0.289241610*wl**2/(wl**2-0.0344239720) + 1.151617340*wl**2/(wl**2-88.4310532))
		if self.type == 'N-KZFS5':
			refractive_index = np.sqrt(1 + 1.47460789*wl**2/(wl**2-0.00986143816) + 0.193584488*wl**2/(wl**2-0.0445477583) + 1.265899740*wl**2/(wl**2-106.4362580))
		if self.type == 'N-BASF2':
			refractive_index = np.sqrt(1 + 1.53652081*wl**2/(wl**2-0.01084357290) + 0.156971102*wl**2/(wl**2-0.0562278762) + 1.301968150*wl**2/(wl**2-131.3397000))
		if self.type == 'N-BASF64':
			refractive_index = np.sqrt(1 + 1.65554268*wl**2/(wl**2-0.01044856440) + 0.171319770*wl**2/(wl**2-0.0499394756) + 1.336644480*wl**2/(wl**2-118.9614720))
		if self.type == 'N-KZFS8':
			refractive_index = np.sqrt(1 + 1.62693651*wl**2/(wl**2-0.01088086300) + 0.243698760*wl**2/(wl**2-0.0494207753) + 1.620071410*wl**2/(wl**2-131.0091630))
		##### LAF #####
		if self.type == 'N-LAF7':
			refractive_index = np.sqrt(1 + 1.74028764*wl**2/(wl**2-0.01079255800) + 0.226710554*wl**2/(wl**2-0.0538626639) + 1.325255480*wl**2/(wl**2-106.2686650))
		if self.type == 'N-LAF2':
			refractive_index = np.sqrt(1 + 1.80984227*wl**2/(wl**2-0.01017116220) + 0.157295550*wl**2/(wl**2-0.0442431765) + 1.093003700*wl**2/(wl**2-100.6877480))
		if self.type == 'N-LAF37':
			refractive_index = np.sqrt(1 + 1.76003244*wl**2/(wl**2-0.00938006396) + 0.248286745*wl**2/(wl**2-0.0360537464) + 1.159351220*wl**2/(wl**2-86.4324693))
		if self.type == 'N-LAF35':
			refractive_index = np.sqrt(1 + 1.51697436*wl**2/(wl**2-0.00750943203) + 0.455875464*wl**2/(wl**2-0.0260046715) + 1.074692420*wl**2/(wl**2-80.5945159))
		if self.type == 'N-LAF34':
			refractive_index = np.sqrt(1 + 1.75836958*wl**2/(wl**2-0.00872810026) + 0.313537785*wl**2/(wl**2-0.0293020832) + 1.189252310*wl**2/(wl**2-85.1780644))
		if self.type == 'N-LAF21':
			refractive_index = np.sqrt(1 + 1.87134529*wl**2/(wl**2-0.00933322280) + 0.250783010*wl**2/(wl**2-0.0345637762) + 1.220486390*wl**2/(wl**2-83.2404866))
		if self.type == 'N-LAF33':
			refractive_index = np.sqrt(1 + 1.79653417*wl**2/(wl**2-0.00927313493) + 0.311577903*wl**2/(wl**2-0.0358201181) + 1.159818630*wl**2/(wl**2-87.3448712))
		##### LASF #####
		if self.type == 'N-LASF9':
			refractive_index = np.sqrt(1 + 2.00029547*wl**2/(wl**2-0.01214260170) + 0.298926886*wl**2/(wl**2-0.0538736236) + 1.80691843*wl**2/(wl**2-156.530829))
		if self.type == 'N-LASF44':
			refractive_index = np.sqrt(1 + 1.78897105*wl**2/(wl**2-0.00872506277) + 0.386758670*wl**2/(wl**2-0.0308085023) + 1.305062430*wl**2/(wl**2-92.7743824))
		if self.type == 'N-LASF43':
			refractive_index = np.sqrt(1 + 1.93502827*wl**2/(wl**2-0.01040014130) + 0.236629350*wl**2/(wl**2-0.0447505292) + 1.262913440*wl**2/(wl**2-87.4375690))
		if self.type == 'N-LASF41':
			refractive_index = np.sqrt(1 + 1.86348331*wl**2/(wl**2-0.00910368219) + 0.413307255*wl**2/(wl**2-0.0339247268) + 1.357848150*wl**2/(wl**2-93.3580595))
		if self.type == 'N-LASF45':
			refractive_index = np.sqrt(1 + 1.87140198*wl**2/(wl**2-0.01121719200) + 0.267777879*wl**2/(wl**2-0.0505134972) + 1.730300080*wl**2/(wl**2-147.1065050))
		if self.type == 'N-LASF31A':
			refractive_index = np.sqrt(1 + 1.96485075*wl**2/(wl**2-0.00982060155) + 0.475231259*wl**2/(wl**2-0.0344713438) + 1.483601090*wl**2/(wl**2-110.7398630))
		if self.type == 'N-LASF40':
			refractive_index = np.sqrt(1 + 1.98550331*wl**2/(wl**2-0.01095833100) + 0.274057042*wl**2/(wl**2-0.0474551603) + 1.289456610*wl**2/(wl**2-96.9085286))
		if self.type == 'N-LASF46A':
			refractive_index = np.sqrt(1 + 2.16701566*wl**2/(wl**2-0.01235955240) + 0.319812761*wl**2/(wl**2-0.0560610282) + 1.660044860*wl**2/(wl**2-107.0477180))
		if self.type == 'N-LASF46B':
			refractive_index = np.sqrt(1 + 2.17988922*wl**2/(wl**2-0.01258053840) + 0.306495184*wl**2/(wl**2-0.0567191367) + 1.568824370*wl**2/(wl**2-105.3165380))
		if self.type == 'N-LASF35':
			refractive_index = np.sqrt(1 + 2.45505861*wl**2/(wl**2-0.01356704040) + 0.453006077*wl**2/(wl**2-0.0545803020) + 2.385130800*wl**2/(wl**2-167.9047150))
		if self.type == 'N-SF6HT':
			refractive_index = np.sqrt(1 + 1.77931763*wl**2/(wl**2-0.0133714182) + 0.338149866*wl**2/(wl**2-0.0617533621) + 2.08734474*wl**2/(wl**2-174.01759))
		if self.type == 'CAF2':
			refractive_index = np.sqrt(1 + 0.617617011*wl**2/(wl**2-0.00275381936) + 0.421117656*wl**2/(wl**2-0.0105900875) + 3.79711183*wl**2/(wl**2-1182.67444))
		##### Others #####
		if self.type == 'AIR':
			refractive_index = 1.0
		
		return refractive_index

# materials = ['N-FK51A', 'N-FK58', 'N-FK5', 'N-PK51', 'N-PK52A', 'N-BK10', 'N-BK7', 'N-PSK3', 'N-PSK53A',
# 			 'N-ZK7', 'N-ZK7A', 'N-K7', 'N-K5', 'N-K10', 'N-KF9', 'N-BAK2', 'N-BAK1', 'N-BAK4', 'N-BALF5',
# 			 'N-KZFS2', 'N-BALF4', 'N-SK11', 'N-SK5', 'N-SK14', 'N-SK16', 'N-SK4', 'N-SK2', 'N-SSK2',
# 			 'N-SSK5', 'N-SSK8', 'N-LAK21', 'N-LAK7', 'N-LAK22', 'N-LAK12', 'N-LAK14', 'N-LAK9', 'N-LAK35',
# 			 'N-LAK34', 'N-LAK8', 'N-LAK10', 'N-LAK33B', 'N-F2', 'N-SF2', 'N-SF5', 'N-SF8', 'N-SF15', 'N-SF1',
# 			 'N-SF10', 'N-SF4', 'N-SF14', 'N-SF11', 'N-SF6', 'N-SF57', 'N-SF66', 'N-BAF10', 'N-BAF52',
# 			 'N-KZFS4', 'N-BAF4', 'N-BAF51', 'N-KZFS11', 'N-KZFS5', 'N-BASF2', 'N-BASF64', 'N-KZFS8', 'N-LAF7',
# 			 'N-LAF2', 'N-LAF37', 'N-LAF35', 'N-LAF34', 'N-LAF21', 'N-LAF33', 'N-LASF9', 'N-LASF44', 'N-LASF43',
# 			 'N-LASF41', 'N-LASF45', 'N-LASF31A', 'N-LASF40', 'N-LASF46A', 'N-LASF46B', 'N-LASF35']

# wla = 0.4861
# wlb = 0.6563

# slopes = []
# for m in materials:
# 	na = GlassMaterial(material=m).disperssion_formula(wla)
# 	nb = GlassMaterial(material=m).disperssion_formula(wlb)
# 	dn = nb - na
# 	dw = wlb - wla
# 	slope = dn/dw
# 	slopes.append(slope)

# for i in range(len(materials)):
# 	print(np.abs(slopes - slopes[i]))

# print(materials[59])
# print(materials[67])
