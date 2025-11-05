"""
Property forms for registration and management.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FloatField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class PropertyRegistrationForm(FlaskForm):
    """Comprehensive form for registering a new property with 80+ fields."""
    
    # ========== LOCATION DETAILS ==========
    state = StringField('State', validators=[DataRequired(), Length(max=100)])
    district = StringField('District', validators=[DataRequired(), Length(max=100)])
    taluka = StringField('Taluka/Tehsil', validators=[Optional(), Length(max=100)])
    village_city = StringField('Village/City', validators=[DataRequired(), Length(max=100)])
    locality = StringField('Locality', validators=[Optional(), Length(max=200)])
    sub_locality = StringField('Sub-Locality', validators=[Optional(), Length(max=200)])
    street_address = TextAreaField('Street Address', validators=[Optional()])
    landmark = StringField('Landmark', validators=[Optional(), Length(max=200)])
    pincode = StringField('Pincode', validators=[Optional(), Length(max=10)])
    ward_number = StringField('Ward Number', validators=[Optional(), Length(max=50)])
    zone = StringField('Zone', validators=[Optional(), Length(max=100)])
    gram_panchayat = StringField('Gram Panchayat', validators=[Optional(), Length(max=200)])
    
    # ========== GPS & MAPPING ==========
    latitude = FloatField('Latitude', validators=[Optional()])
    longitude = FloatField('Longitude', validators=[Optional()])
    altitude = FloatField('Altitude (meters)', validators=[Optional()])
    
    # ========== LAND MEASUREMENTS ==========
    survey_number = StringField('Survey Number', validators=[Optional(), Length(max=100)])
    plot_number = StringField('Plot Number', validators=[Optional(), Length(max=100)])
    block_number = StringField('Block Number', validators=[Optional(), Length(max=100)])
    khasra_number = StringField('Khasra Number', validators=[Optional(), Length(max=100)])
    
    area = FloatField('Total Area', validators=[DataRequired(), NumberRange(min=0.01)])
    area_unit = SelectField('Area Unit', choices=[
        ('sqm', 'Square Meters'),
        ('sqft', 'Square Feet'),
        ('acre', 'Acres'),
        ('hectare', 'Hectares'),
        ('gunta', 'Gunta'),
        ('bigha', 'Bigha')
    ], validators=[DataRequired()])
    
    length = FloatField('Length', validators=[Optional(), NumberRange(min=0)])
    width = FloatField('Width', validators=[Optional(), NumberRange(min=0)])
    road_frontage = FloatField('Road Frontage', validators=[Optional(), NumberRange(min=0)])
    frontage_direction = SelectField('Frontage Direction', choices=[
        ('', 'Select'),
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], validators=[Optional()])
    
    plot_shape = SelectField('Plot Shape', choices=[
        ('', 'Select'),
        ('rectangular', 'Rectangular'),
        ('square', 'Square'),
        ('irregular', 'Irregular'),
        ('triangular', 'Triangular'),
        ('l_shaped', 'L-Shaped')
    ], validators=[Optional()])
    
    terrain_type = SelectField('Terrain Type', choices=[
        ('', 'Select'),
        ('flat', 'Flat'),
        ('sloping', 'Sloping'),
        ('hilly', 'Hilly'),
        ('undulating', 'Undulating')
    ], validators=[Optional()])
    
    built_up_area = FloatField('Built-up Area', validators=[Optional(), NumberRange(min=0)])
    carpet_area = FloatField('Carpet Area', validators=[Optional(), NumberRange(min=0)])
    
    # ========== BOUNDARIES ==========
    north_boundary = StringField('North Boundary', validators=[Optional(), Length(max=200)])
    south_boundary = StringField('South Boundary', validators=[Optional(), Length(max=200)])
    east_boundary = StringField('East Boundary', validators=[Optional(), Length(max=200)])
    west_boundary = StringField('West Boundary', validators=[Optional(), Length(max=200)])
    
    # ========== PROPERTY CLASSIFICATION ==========
    property_type = SelectField('Property Type', choices=[
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('agricultural', 'Agricultural'),
        ('industrial', 'Industrial'),
        ('institutional', 'Institutional'),
        ('mixed_use', 'Mixed Use')
    ], validators=[DataRequired()])
    
    sub_property_type = StringField('Sub-Type (Villa/Apartment/Farmhouse)', validators=[Optional(), Length(max=100)])
    land_category_id = SelectField('Land Category', coerce=int, validators=[Optional()])
    usage_type_id = SelectField('Usage Type', coerce=int, validators=[Optional()])
    current_land_use = StringField('Current Land Use', validators=[Optional(), Length(max=200)])
    zoning_classification = StringField('Zoning Classification', validators=[Optional(), Length(max=100)])
    
    property_nature = SelectField('Property Nature', choices=[
        ('', 'Select'),
        ('urban', 'Urban'),
        ('rural', 'Rural'),
        ('semi_urban', 'Semi-Urban')
    ], validators=[Optional()])
    
    property_age_years = FloatField('Property Age (Years)', validators=[Optional(), NumberRange(min=0)])
    property_condition = SelectField('Property Condition', choices=[
        ('', 'Select'),
        ('new', 'New'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor')
    ], validators=[Optional()])
    
    occupancy_status = SelectField('Occupancy Status', choices=[
        ('', 'Select'),
        ('owner_occupied', 'Owner Occupied'),
        ('tenant', 'Tenant Occupied'),
        ('vacant', 'Vacant'),
        ('under_construction', 'Under Construction')
    ], validators=[Optional()])
    
    # ========== CONSTRUCTION DETAILS ==========
    number_of_floors = FloatField('Number of Floors', validators=[Optional(), NumberRange(min=0)])
    number_of_bedrooms = FloatField('Number of Bedrooms', validators=[Optional(), NumberRange(min=0)])
    number_of_bathrooms = FloatField('Number of Bathrooms', validators=[Optional(), NumberRange(min=0)])
    number_of_kitchens = FloatField('Number of Kitchens', validators=[Optional(), NumberRange(min=0)])
    parking_spaces = FloatField('Parking Spaces', validators=[Optional(), NumberRange(min=0)])
    
    construction_type = SelectField('Construction Type', choices=[
        ('', 'Select'),
        ('rcc', 'RCC Frame'),
        ('load_bearing', 'Load Bearing'),
        ('steel_frame', 'Steel Frame'),
        ('prefab', 'Prefabricated')
    ], validators=[Optional()])
    
    flooring_type = StringField('Flooring Type (Marble/Tiles/Wooden)', validators=[Optional(), Length(max=200)])
    year_of_construction = FloatField('Year of Construction', validators=[Optional(), NumberRange(min=1800, max=2100)])
    
    # ========== SOIL & AGRICULTURE ==========
    soil_type = SelectField('Soil Type', choices=[
        ('', 'Select'),
        ('red', 'Red Soil'),
        ('black', 'Black Soil'),
        ('alluvial', 'Alluvial'),
        ('sandy', 'Sandy'),
        ('clayey', 'Clayey'),
        ('loamy', 'Loamy')
    ], validators=[Optional()])
    
    soil_quality = SelectField('Soil Quality', choices=[
        ('', 'Select'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor')
    ], validators=[Optional()])
    
    irrigation_type = StringField('Irrigation Type (Well/Canal/Drip)', validators=[Optional(), Length(max=200)])
    current_crop = StringField('Current Crop', validators=[Optional(), Length(max=200)])
    tree_count = FloatField('Number of Trees', validators=[Optional(), NumberRange(min=0)])
    
    # ========== WATER RESOURCES ==========
    water_source = SelectField('Water Source', choices=[
        ('', 'Select'),
        ('municipal', 'Municipal Supply'),
        ('borewell', 'Borewell'),
        ('open_well', 'Open Well'),
        ('river', 'River/Canal'),
        ('tanker', 'Water Tanker')
    ], validators=[Optional()])
    
    borewell_depth_ft = FloatField('Borewell Depth (feet)', validators=[Optional(), NumberRange(min=0)])
    water_supply_hours_per_day = FloatField('Water Supply Hours/Day', validators=[Optional(), NumberRange(min=0, max=24)])
    
    # ========== ELECTRICITY & UTILITIES ==========
    electricity_connection_type = SelectField('Electricity Connection', choices=[
        ('', 'Select'),
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('none', 'No Connection')
    ], validators=[Optional()])
    
    electricity_load_kw = FloatField('Electricity Load (KW)', validators=[Optional(), NumberRange(min=0)])
    electricity_meter_number = StringField('Electricity Meter Number', validators=[Optional(), Length(max=100)])
    
    # ========== ROAD & ACCESS ==========
    road_access = SelectField('Road Access', choices=[
        ('', 'Select'),
        ('direct', 'Direct Road Access'),
        ('common_path', 'Through Common Path'),
        ('no_direct_access', 'No Direct Access')
    ], validators=[Optional()])
    
    road_type = SelectField('Road Type', choices=[
        ('', 'Select'),
        ('paved', 'Paved/Tar Road'),
        ('cement', 'Cement Road'),
        ('unpaved', 'Unpaved/Kuccha Road'),
        ('mud', 'Mud Road')
    ], validators=[Optional()])
    
    road_width_ft = FloatField('Road Width (feet)', validators=[Optional(), NumberRange(min=0)])
    distance_from_main_road_km = FloatField('Distance from Main Road (km)', validators=[Optional(), NumberRange(min=0)])
    
    # ========== AMENITIES ==========
    has_compound_wall = SelectField('Compound Wall', choices=[('', 'Select'), ('yes', 'Yes'), ('no', 'No')], validators=[Optional()])
    has_main_gate = SelectField('Main Gate', choices=[('', 'Select'), ('yes', 'Yes'), ('no', 'No')], validators=[Optional()])
    has_security = SelectField('Security', choices=[('', 'Select'), ('yes', 'Yes'), ('no', 'No')], validators=[Optional()])
    
    # ========== VALUATION ==========
    market_value = FloatField('Market Value (₹)', validators=[Optional(), NumberRange(min=0)])
    registered_value = FloatField('Registered Value (₹)', validators=[Optional(), NumberRange(min=0)])
    stamp_duty_paid = FloatField('Stamp Duty Paid (₹)', validators=[Optional(), NumberRange(min=0)])
    registration_fee_paid = FloatField('Registration Fee Paid (₹)', validators=[Optional(), NumberRange(min=0)])
    
    # ========== LEGAL & COMPLIANCE ==========
    encumbrance_status = SelectField('Encumbrance Status', choices=[
        ('', 'Select'),
        ('clear', 'Clear/Unencumbered'),
        ('mortgaged', 'Mortgaged'),
        ('disputed', 'Disputed'),
        ('leased', 'Leased')
    ], validators=[Optional()])
    
    legal_issues = TextAreaField('Legal Issues (if any)', validators=[Optional()])
    
    # ========== ADDITIONAL INFO ==========
    description = TextAreaField('Additional Description/Notes', validators=[Optional()])
    special_features = TextAreaField('Special Features', validators=[Optional()])
    
    # ========== DOCUMENTS ==========
    document1 = FileField('Sale Deed/Title Deed', validators=[
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF and image files allowed')
    ])
    document2 = FileField('Identity Proof', validators=[
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF and image files allowed')
    ])
    document3 = FileField('Property Tax Receipt', validators=[
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF and image files allowed')
    ])


class PropertySearchForm(FlaskForm):
    """Form for searching properties."""
    
    search_query = StringField('Search', validators=[Optional()])
    state = StringField('State', validators=[Optional()])
    district = StringField('District', validators=[Optional()])
    village_city = StringField('Village/City', validators=[Optional()])
    property_type = SelectField('Property Type', choices=[
        ('', 'All Types'),
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('agricultural', 'Agricultural'),
        ('industrial', 'Industrial'),
        ('institutional', 'Institutional')
    ], validators=[Optional()])
    status = SelectField('Status', choices=[
        ('', 'All Status'),
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active')
    ], validators=[Optional()])


class PropertyApprovalForm(FlaskForm):
    """Form for approving/rejecting properties."""
    
    action = SelectField('Action', choices=[
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('request_info', 'Request Information')
    ], validators=[DataRequired()])
    
    comments = TextAreaField('Comments/Reason', validators=[DataRequired(), Length(min=10, max=1000)])
