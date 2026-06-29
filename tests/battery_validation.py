def test_battery_performance():
    """Validate battery performance for both fungal strains (T. pubescens and P. chrysosporium)."""
    t_pubescens_data = load_strain_data('T_pubescens')
    p_chrysosporium_data = load_strain_data('P_chrysosporium')
    
    t_power = calculate_power_output(t_pubescens_data, temp=25, humidity=60)
    p_power = calculate_power_output(p_chrysosporium_data, temp=25, humidity=60)
    
    assert abs(t_power - 12.5) / 12.5 < 0.2
    assert p_power > 150
    
    t_power_alt = calculate_power_output(t_pubescens_data, temp=20, humidity=80)
    p_power_alt = calculate_power_output(p_chrysosporium_data, temp=20, humidity=80)
    
    assert t_power_alt > t_power * 0.8
    assert p_power_alt > p_power * 0.8
    
    return {
        't_pubescens_power': t_power,
        'p_chrysosporium_power': p_power,
        'performance_valid': True
    }
