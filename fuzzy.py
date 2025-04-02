import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import textwrap
from datetime import datetime

# fuzzy system for an automatic sprinkler


# We define inputs: Soil Moisture and Temperature, and an output: Water Sprinkling Level

soil_moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'Soil Moisture')
temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'Temperature')
water_sprinkle = ctrl.Consequent(np.arange(0, 101, 1), 'Water Sprinkling')

# Now each input can be categorized using membership functions
soil_moisture['dry'] = fuzz.trimf(soil_moisture.universe, [0, 0, 50])
soil_moisture['moist'] = fuzz.trimf(soil_moisture.universe, [20, 50, 80])
soil_moisture['wet'] = fuzz.trimf(soil_moisture.universe, [50, 100, 100])

temperature['cold'] = fuzz.trimf(temperature.universe, [0, 0, 20])
temperature['warm'] = fuzz.trimf(temperature.universe, [10, 25, 40])
temperature['hot'] = fuzz.trimf(temperature.universe, [30, 50, 50])

water_sprinkle['low'] = fuzz.trimf(water_sprinkle.universe, [0, 0, 50])
water_sprinkle['medium'] = fuzz.trimf(water_sprinkle.universe, [20, 50, 80])
water_sprinkle['high'] = fuzz.trimf(water_sprinkle.universe, [50, 100, 100])

#We define some rules for the system
rule1 = ctrl.Rule(soil_moisture['dry'] & temperature['hot'], water_sprinkle['high'])
rule2 = ctrl.Rule(soil_moisture['dry'] & temperature['warm'], water_sprinkle['medium'])
rule3 = ctrl.Rule(soil_moisture['moist'] & temperature['warm'], water_sprinkle['medium'])
rule4 = ctrl.Rule(soil_moisture['moist'] & temperature['cold'], water_sprinkle['low'])
rule5 = ctrl.Rule(soil_moisture['wet'], water_sprinkle['low'])

# Applying the rules 
sprinkle_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
sprinkler = ctrl.ControlSystemSimulation(sprinkle_ctrl)

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# Add membership function plots
plt.figure(figsize=(12, 8))
plt.subplot(311)
soil_moisture.view()
plt.title('Soil Moisture Membership Functions')
plt.savefig('screenshots/soil_moisture_mf.png')
plt.close()

plt.figure(figsize=(12, 8))
plt.subplot(311)
temperature.view()
plt.title('Temperature Membership Functions')
plt.savefig('screenshots/temperature_mf.png')
plt.close()

plt.figure(figsize=(12, 8))
plt.subplot(311)
water_sprinkle.view()
plt.title('Water Sprinkling Membership Functions')
plt.savefig('screenshots/water_sprinkle_mf.png')
plt.close()

# Running the system with multiple test cases
test_cases = [
    (30, 35), # Hot day, moderate soil moisture
    (70, 20), # Cool day, high soil moisture
    (10, 40), # Hot day, very dry soil
    (50, 10), # Cold day, moderate soil moisture
    (80, 30), # Warm day, high soil moisture
    (20, 45), # Very hot day, dry soil
    (90, 15), # Cool day, very wet soil
    (40, 25), # Moderate temperature, moderate moisture
    (15, 35), # Hot day, dry soil
    (60, 5),  # Very cold day, moderate moisture
]

for i, (soil, temp) in enumerate(test_cases):
    sprinkler.input['Soil Moisture'] = soil
    sprinkler.input['Temperature'] = temp
    sprinkler.compute()
    
    # Plot the result for better visualization
    plt.figure()
    plt.title(f'Soil: {soil}% | Temp: {temp}°C | Sprinkle: {sprinkler.output["Water Sprinkling"]:.2f}%')
    plt.xlabel("Inputs")
    plt.ylabel("Sprinkling Intensity")
    plt.bar(["Dry", "Moist", "Wet"], fuzz.interp_membership(soil_moisture.universe, soil_moisture['dry'].mf, soil))
    plt.bar(["Cold", "Warm", "Hot"], fuzz.interp_membership(temperature.universe, temperature['cold'].mf, temp))
    plt.bar(["Low", "Medium", "High"], fuzz.interp_membership(water_sprinkle.universe, water_sprinkle['low'].mf, sprinkler.output['Water Sprinkling']))
    
    # Save each output as a screenshot
    screenshot_path = f'screenshots/output_{i}.png'
    plt.savefig(screenshot_path)
    plt.close()

# Enhanced PDF generation
try:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title page
    pdf.add_page()
    try:
        pdf.add_font("Book Antiqua", style="", fname="fonts/bookantiqua.ttf", uni=True)
        pdf.add_font("Book Antiqua", style="B", fname="fonts/bookantiqua_bold.ttf", uni=True)
        font_name = "Book Antiqua"
        default_font_size = 12
    except Exception as e:
        print(f"Error loading fonts: {str(e)}. Using Arial instead.")
        font_name = "Arial"
        default_font_size = 12

    # Title page content
    pdf.set_font(font_name, 'B', size=24)
    pdf.cell(200, 40, "Fuzzy Logic Sprinkler System", ln=True, align='C')
    pdf.ln(20)
    
    # Team information with consistent 12pt font
    pdf.set_font(font_name, 'B', size=default_font_size)
    pdf.cell(200, 10, "Team Members:", ln=True)
    pdf.set_font(font_name, '', size=default_font_size)
    team_members = [
        "WAINAINA, NIXON MBURU – 665507",
        "WILLIAM MUNGAI – 666494",
        "BRACKCIDIS TEMKO – 666989",
        "LEE KAMAU – 666591",
        "STEPHEN KAHANYA 668435"
    ]
    for member in team_members:
        pdf.cell(200, 10, member, ln=True)
    pdf.ln(10)

    # Date
    pdf.cell(200, 10, f"Date: {datetime.now().strftime('%B %d, %Y')}", ln=True)
    
    # Enhanced sections with more detailed content
    sections = {
        "Introduction": """This report presents an advanced fuzzy logic-based sprinkler control system designed to optimize irrigation based on environmental conditions. The system demonstrates the practical application of fuzzy logic in agricultural automation, providing intelligent and efficient water management.

The primary advantage of this fuzzy logic approach is its ability to handle imprecise input data and provide smooth, continuous output adjustments, unlike traditional binary systems. This results in more natural and efficient irrigation control.""",

        "System Description": """The intelligent sprinkler system incorporates multiple components working in harmony:

Input Variables:
1. Soil Moisture (0-100%): Measures water content in soil
   • Dry (0-50%): Indicates urgent watering needs
   • Moist (20-80%): Optimal moisture range
   • Wet (50-100%): Sufficient water content

2. Temperature (0-50°C): Monitors environmental temperature
   • Cold (0-20°C): Low evaporation conditions
   • Warm (10-40°C): Moderate water requirements
   • Hot (30-50°C): High evaporation risk

Output Control:
• Water Sprinkling Level (0-100%): Automated adjustment based on conditions
   • Low (0-50%): Conservative water usage
   • Medium (20-80%): Balanced irrigation
   • High (50-100%): Intensive watering""",

        "Methodology": """The system employs triangular membership functions for both inputs and outputs, providing a balanced approach to fuzzy set representation. The rule base is designed to prioritize water conservation while maintaining optimal growing conditions.

Key Implementation Features:
1. Continuous variable monitoring
2. Real-time adjustment capability
3. Smooth transition between states
4. Adaptive response to changing conditions""",
    }

    # Add enhanced sections to PDF
    for title, content in sections.items():
        pdf.add_page()
        pdf.set_font(font_name, 'B', size=16)
        pdf.cell(200, 10, title, ln=True)
        pdf.set_font(font_name, '', size=default_font_size)
        pdf.multi_cell(0, 10, content)

    # Add Implementation Screenshots section
    pdf.add_page()
    pdf.set_font(font_name, 'B', size=16)
    pdf.cell(200, 10, "Implementation Screenshots", ln=True)
    pdf.set_font(font_name, '', size=default_font_size)
    pdf.multi_cell(0, 5, "The following screenshots show the system implementation and key components:")
    
    # Add the three screenshots with captions
    screenshots = [
        ("Screenshot from 2025-03-23 14-12-50.png", "System Components and Variables"),
        ("Screenshot from 2025-03-23 14-13-19.png", "Membership Functions Implementation"),
        ("Screenshot from 2025-03-23 14-13-47.png", "Rule Base and Control System")
    ]
    
    for img_file, caption in screenshots:
        pdf.ln(5)
        pdf.image(img_file, x=10, w=190)
        pdf.set_font(font_name, 'B', size=default_font_size)
        pdf.ln(2)
        pdf.cell(200, 10, caption, ln=True, align='C')
        pdf.ln(5)

    # Add membership function plots to PDF
    pdf.add_page()
    pdf.set_font(font_name, 'B', size=16)
    pdf.cell(200, 10, "System Membership Functions", ln=True)
    pdf.image('screenshots/soil_moisture_mf.png', x=10, w=180)
    pdf.image('screenshots/temperature_mf.png', x=10, w=180)
    pdf.image('screenshots/water_sprinkle_mf.png', x=10, w=180)

    # Add rule explanation section
    pdf.add_page()
    pdf.set_font(font_name, 'B', size=16)
    pdf.cell(200, 10, "Fuzzy Rule Base Design", ln=True)
    
    # Rule explanations with better spacing
    rules = [
        ("Rule 1", "IF soil is dry AND temperature is hot", "THEN sprinkle high",
         "High temperature combined with dry soil requires maximum irrigation"),
        
        ("Rule 2", "IF soil is dry AND temperature is warm", "THEN sprinkle medium",
         "Warm conditions with dry soil need moderate watering"),
        
        ("Rule 3", "IF soil is moist AND temperature is warm", "THEN sprinkle medium",
         "Optimal moisture maintenance during warm weather"),
        
        ("Rule 4", "IF soil is moist AND temperature is cold", "THEN sprinkle low",
         "Cold weather reduces evaporation need"),
        
        ("Rule 5", "IF soil is wet", "THEN sprinkle low",
         "Wet soil needs minimal watering regardless of temperature")
    ]
    
    for rule_num, condition, action, explanation in rules:
        pdf.ln(5)
        pdf.set_font(font_name, 'B', size=default_font_size)
        pdf.cell(200, 6, rule_num, ln=True)
        pdf.set_font(font_name, '', size=default_font_size)
        pdf.cell(200, 6, condition, ln=True)
        pdf.cell(200, 6, action, ln=True)
        pdf.cell(200, 6, f"Explanation: {explanation}", ln=True)

    # Enhanced test results with detailed analysis
    pdf.add_page()
    pdf.set_font(font_name, 'B', size=16)
    pdf.cell(200, 10, "Test Results and Analysis", ln=True)
    
    for i, (soil, temp) in enumerate(test_cases):
        sprinkler.input['Soil Moisture'] = soil
        sprinkler.input['Temperature'] = temp
        sprinkler.compute()
        
        pdf.set_font(font_name, 'B', size=14)
        pdf.cell(200, 10, f"Test Case {i+1}", ln=True)
        pdf.set_font(font_name, '', size=default_font_size)
        
        analysis = f"""Environmental Conditions:
• Soil Moisture: {soil}% - {'Very Dry' if soil < 20 else 'Dry' if soil < 40 else 'Moderate' if soil < 60 else 'Wet' if soil < 80 else 'Very Wet'}
• Temperature: {temp}°C - {'Cold' if temp < 15 else 'Cool' if temp < 25 else 'Warm' if temp < 35 else 'Hot'}

System Response:
• Sprinkling Level: {sprinkler.output['Water Sprinkling']:.1f}%
• Reasoning: {
    'High water need due to dry soil and high temperature' if soil < 40 and temp > 30
    else 'Moderate watering to maintain moisture' if 40 <= soil <= 60
    else 'Minimal watering needed due to sufficient soil moisture' if soil > 60
    else 'Balanced watering based on conditions'
}"""
        pdf.multi_cell(0, 10, analysis)
        
        if os.path.exists(f'screenshots/output_{i}.png'):
            pdf.image(f'screenshots/output_{i}.png', x=10, w=180)
        pdf.ln(10)

    # Conclusion
    pdf.add_page()
    pdf.set_font(font_name, 'B', size=16)
    pdf.cell(200, 10, "Conclusion", ln=True)
    pdf.set_font(font_name, '', size=12)
    conclusion_text = """The fuzzy logic sprinkler system demonstrates effective decision-making capabilities in determining appropriate water sprinkling levels based on environmental conditions. The system successfully adapts to various combinations of soil moisture and temperature, providing an intelligent solution for automated irrigation control. The membership functions and rule base ensure smooth transitions between different sprinkling levels, avoiding abrupt changes that could stress the plants or waste water."""
    pdf.multi_cell(0, 10, conclusion_text)

    # Save the report
    pdf.output("Fuzzy_Logic_Report.pdf")
    print("Enhanced report generated: Fuzzy_Logic_Report V1.4.pdf")

except Exception as e:
    print(f"Error generating PDF report: {str(e)}")

# Cleanup
plt.close('all')
