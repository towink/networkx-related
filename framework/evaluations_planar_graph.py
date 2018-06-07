from .evaluation_oracle import EvaluationOracle

# see sage worksheet "sage-notebook.ipynb"

planar_graph_evals = {
    'D(x*G_1_dx(x,y),y)': 1.09347848647472549211184239941769601061,
    'D_dx(x*G_1_dx(x,y),y)': 3.45102206434801157864803811245239712851,
    'G_1(x,y)': 0.0372484305053690456202661877963311349072,
    'G_1_dx(x,y)': 1.03960692373287371278312170556092216601,
    'G_1_dx_dx(x,y)': 1.1831386535487874823112196643179832576,
    'G_2_dx(x*G_1_dx(x,y),y)': 0.038842683760013258631145523348425252874,
    'G_2_dx_dx(x*G_1_dx(x,y),y)': 1.05099440303963997980334319688998807042,
    'G_3_arrow_dy(x*G_1_dx(x,y),D_dx(x*G_1_dx(x,y),y))': 0.000136114085896582,
    'H(x*G_1_dx(x,y),y)': 0.00206469524549284585247141356302904687086,
    'H_dx(x*G_1_dx(x,y),y)': 0.276441303522129889594403984833856178203,
    'J_a(x*G_1_dx(x,y),D(x*G_1_dx(x,y),y))': 6.51755944546283654118400704909007336485e-6,
    'J_a_dx(x*G_1_dx(x,y),D(x*G_1_dx(x,y),y))': 0.00101670701121470916578733450493266048102,
    'K(x*G_1_dx(x,y),D(x*G_1_dx(x,y),y))': 0.212193853436531,
    'K_dx(x*G_1_dx(x,y),D(x*G_1_dx(x,y),y))': 15.4865762511452,
    'P(x*G_1_dx(x,y),y)': 0.0477986369539869322752735578478273809975,
    'P_dx(x*G_1_dx(x,y),y)': 1.80255895061461154228734452882283065547,
    'R_b(x*G_1_dx(x,y),D(x*G_1_dx(x,y),y))': 0.512029288702929,
    'R_w(x*G_1_dx(x,y),D(x*G_1_dx(x,y),y))': 2.57765531062124,
    'S(x*G_1_dx(x,y),y)': 0.0436151542752457139840974280068395827400,
    'S_dx(x*G_1_dx(x,y),y)': 1.37202181021127014676628959879571029484,
    'x': 0.0365447705189290291920092340981152311040,
    'x*G_1_dx(x,y)': 0.0379921964577076229466965829549486315897,
    'y': 1.00000000000000
}

planar_graph_oracle = EvaluationOracle()
planar_graph_oracle.add_evals(planar_graph_evals)