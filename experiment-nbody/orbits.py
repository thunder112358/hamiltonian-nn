# Hamiltonian Neural Networks | 2019
# Sam Greydanus, Misko Dzamba, Jason Yosinski

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate

def get_accelerations(bodies):
    n = bodies.shape[0] # number of bodies
    net_accs = [] # [nbodies x  2 (a_x, a_y)]
    for body in range(n):
        other_bodies = np.concatenate([bodies[:body, :], bodies[body+1:, :]], axis=0)
        displacements = other_bodies[:, 1:3] - bodies[body, 1:3] # indexes 1:3 -> pxs, pys
        distances = (displacements**2).sum(1, keepdims=True)**0.5
        masses = other_bodies[:, 0:1] # index 0 -> mass
        pointwise_accs = masses * displacements / distances**3 # G = 1
        net_acc = pointwise_accs.sum(0, keepdims=True)
        net_accs.append(net_acc)
    net_accs = np.concatenate(net_accs, axis=0)
    return net_accs

def update_fn(t, flat_state):
    state = flat_state.reshape(-1,5)
    mass_update = np.zeros_like(state[:,:1])
    vels = state[:,3:]
    accs = get_accelerations(state)
    
    new_bodies = np.concatenate([mass_update, vels, accs], axis=-1)
    return new_bodies.flatten()

def custom_init(): # each body has state: [mass, px, py, vx, vy]
    bodies = np.zeros((3,5)) # three bodies with state info ~ [mass, px, py, vx, vy]
    bodies[0,:] = np.asarray([1, 1, 0.3, 0,  0.1]) # body 1
    bodies[1,:] = np.asarray([2, 0.0, 0.3, 0.1, 0]) # body 2
    bodies[2,:] = np.asarray([3, 0.1, 0.3, 0.1,  -0.3])
    return bodies

def custom_init_2d(same_mass=False): # each body has state: [mass, px, py, vx, vy]
    bodies = np.zeros((2,5)) # three bodies with state info ~ [mass, px, py, vx, vy]
    m1,m2,vx,vy=np.random.rand(4)
    if same_mass:
        m2=m1
    vx/=2
    vy/=2
    bodies[0,:] = np.asarray([m1, 1, 0, vx, vy]) # body 1
    bodies[1,:] = np.asarray([m2, -1, 0, -vx/(m2/m1), -vy/(m2/m1)]) # body 2
    kinetic_energy=(0.5*bodies[:,0]*(bodies[:,-2:]**2).sum(axis=0)).sum()
    G=1
    gravitational_energy=G*m1*m2/2
    #if too much energy lets try again
    if kinetic_energy>gravitational_energy:
      return custom_init_2d()
    return bodies

def special_triplet():
    bodies = np.zeros((3,5)) # three bodies with state info ~ [mass, px, py, vx, vy]
    bodies[0,:] = np.asarray([4, 0, 0, 0, -1/np.sqrt(2)]) # body 1
    bodies[1,:] = np.asarray([4, 1, 0, 0,  1/np.sqrt(2)]) # body 2
    bodies[2,:] = np.asarray([1e-4, 0.5, np.sqrt(3)/2, -np.sqrt(3/2), 0]) # body 3
    return bodies

def get_3body_orbit(c='IA',n=0):
    v1,v2,T=orbits[c][n]
    bodies = np.zeros((3,5)) # three bodies with state info ~ [mass, px, py, vx, vy]
    bodies[0,:] = np.asarray([1, -1, 0, v1, v2]) # body 1
    bodies[1,:] = np.asarray([1, 1, 0, v1,  v2]) # body 2
    bodies[2,:] = np.asarray([0.5, 0, 0, -2*v1/0.5, -2*v2/0.5]) # body 3
    return bodies.flatten(),T

orbits={
#IA
'IA': (
(0.2869236336,0.0791847624,4.1761292190),
(0.3420307307,0.1809369236,13.9153339459),
(0.3697718457,0.1910065395,25.9441952945),
(0.2009656237,0.2431076328,19.0134164290),
(0.2613236072,0.2356235235,28.4358575383),
(0.1908428490,0.1150772110,15.9682350284),
(0.1579313682,0.0949852732,14.5766076405),
(0.0979965852,0.0369408875,15.6059191780),
(0.3589116510,0.0578397225,35.2777168591),
(0.2066204352,0.1123859298,22.8770013381),
(0.3095805649,0.1012188182,37.8353981553),
(0.2935606362,0.2168613674,54.5846159117),
(0.2614113685,0.1097599351,39.2849176561),
(0.3049866810,0.0979042378,46.1065937257),
(0.1644199050,0.0637816144,29.0215071279),
(0.2698142826,0.0360688014,37.8687787781),
(0.1451647294,0.0318334148,30.5079373557),
(0.3467747647,0.0474429378,59.7722919460),
(0.3025694869,0.0951546278,54.5401904272),
(0.2726720005,0.0478754379,46.2148464304),
(0.2997637007,0.0934329270,62.7105115603),
(0.2747511246,0.0544869553,54.5744279508),
(0.2867479329,0.0521752523,57.0633556930),
(0.2172290935,0.0383448898,45.1666009592),
(0.3108794721,0.1023369865,71.4799545005),
(0.2979925625,0.0918951185,70.9842467059),
(0.2366779591,0.0914177522,56.6833946453),
(0.1628551705,0.0589464762,46.2097799724),
(0.2763361520,0.0588302447,62.9447137981),
(0.1936757357,0.0730232621,49.7181917085),
(0.3017504100,0.1030778699,77.7653686390),
(0.1671144104,0.0438815944,49.1675240282),
(0.3274705985,0.0612651208,84.0143824473),
(0.2668455153,0.0138391891,63.2419174415),
(0.3220251063,0.0754954232,87.6821712800),
(0.2965579937,0.0906370328,79.2439520137),
(0.2775882955,0.0619333069,71.3240509215),
(0.3558062278,0.0405108521,108.4971611336),
(0.3060017590,0.0986219478,88.0890690057),
(0.2689229383,0.0312527426,71.5697332821),
(0.1317126561,0.0254909293,51.5736578935),
(0.1428972736,0.0445901978,55.4783856796),
(0.3132151994,0.1046181562,96.6632360131),
(0.2954964679,0.0895434067,87.5354654697),
(0.2749526022,0.0648656500,78.6571356819) ),
'IB': (
(0.2374365149,0.2536896353,8.5581422789),
(0.2707702758,0.2974619413,19.9858290667),
(0.1804341862,0.0774390466,10.5764781985),
(0.0548520001,0.3291535443,20.9927052014),
(0.2817159946,0.3093138094,31.1291374576),
(0.2679384847,0.0246961144,16.8511048757),
(0.2674226718,0.2139289499,23.9372167355),
(0.2878430093,0.3151477978,42.2778567687),
(0.3030963188,0.0966599779,25.1036320618),
(0.1099852485,0.0308448543,14.5241562996),
(0.2291294485,0.2119828182,24.7437423714),
(0.3692649167,0.0417694147,34.2771859316),
(0.2737871583,0.0515706441,25.1965811355),
(0.2988140236,0.0926281921,33.4227154398),
(0.2788426894,0.0601828236,33.7944313342),
(0.2790832581,0.2276230751,50.6192127242),
(0.2163072511,0.0457824324,27.4550707427),
(0.2631918196,0.0971022505,36.9742814503),
(0.1940565085,0.0716923953,29.5220753291),
(0.2790460219,0.0652447476,41.9537927832),
(0.1166234512,0.0062473070,27.8908904718),
(0.2941922385,0.0882015308,49.9756827423),
(0.1482620649,0.0469161409,32.2082149709),
(0.3383350929,0.0633820096,60.3349978637),
(0.3086986007,0.1005760508,58.8260422524),
(0.2804820502,0.0682367913,50.3545241044),
(0.2928957198,0.0867806393,58.2512450352),
(0.3121801357,0.0954940881,68.9135784414),
(0.2815530004,0.0703169410,58.7667019161),
(0.2702462061,0.0720377706,56.4003264775),
(0.2131987197,0.0555522173,46.7195262030),
(0.1832565230,0.0627595131,46.7521066510),
(0.2919082649,0.0856563914,66.5195343482),
(0.2703631586,0.0386904791,58.8880393273),
(0.1859380756,0.0731374234,50.3601763743),
(0.2489094150,0.0992895950,61.2653969718),
(0.2823888686,0.0718580778,67.1889348357),
(0.1615485916,0.0277748182,46.9823741559),
(0.2911309221,0.0847384936,74.7822861358),
(0.1771098445,0.0784887228,52.5734020100),
(0.1838565013,0.0752899792,53.1629113586),
(0.2143486812,0.0918266864,58.0738450139),
(0.3247862862,0.0695897171,85.9588123017),
(0.1610459823,0.0516375322,50.2179896145),
(0.2722601340,0.0464077813,67.2341769532),
(0.3192498609,0.0879575434,90.1594809343),
(0.2830620767,0.0730518241,75.6195474605),
(0.2905035826,0.0839717300,83.0409561905),
(0.3002585565,0.1059795568,88.9553085721),
(0.2174816082,0.0342966208,62.8453538957) ),
'IIC': (
(0.2057599772,0.2910772545,16.4482452694),
(0.0621756721,0.0261903906,6.2854133740),
(0.0657658390,0.1124034346,8.0617096205),
(0.0169747300,0.0752136850,8.8877784855),
(0.2251711660,0.3443496457,32.8998590701),
(0.1194732446,0.0207612630,10.6764792286),
(0.0551050358,0.3697557117,28.5843693576),
(0.0108740090,0.3192205525,25.7212160836),
(0.3448435595,0.0697188543,24.6216211722),
(0.0117243540,0.3525284661,28.5310959155),
(0.1780039242,0.2004919509,16.5294086907),
(0.1282291061,0.3649372977,40.6015240363),
(0.3234173131,0.2471156877,44.4546188773),
(0.2104677107,0.1057158539,18.2820987595),
(0.1983865989,0.1226004003,19.7881493182),
(0.2287935035,0.0923297799,22.5126057181),
(0.0913811473,0.0093493963,16.8086808175),
(0.2383747181,0.2447155547,35.0733137252),
(0.0992256924,0.0269686482,18.2257172127),
(0.3345991412,0.0565118924,35.7753676955),
(0.1490452956,0.0531097638,21.0786048660),
(0.2263132666,0.0992959988,25.8750904330),
(0.1822531374,0.1005779979,22.9574138909),
(0.3130939094,0.0872917851,35.4487192804),
(0.2379407604,0.2522685220,44.6369551897),
(0.1230951336,0.0496740170,21.5462119008),
(0.1326230917,0.0945397322,24.0011090101),
(0.1440416968,0.1072211552,24.7755961375),
(0.1444470268,0.0693298831,25.2083739245),
(0.3196418099,0.1040424691,47.3539072837) )
}
