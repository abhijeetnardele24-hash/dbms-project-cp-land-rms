"""
ULTRA COMPREHENSIVE Property Model
Collects extensive information about land/property
150+ fields for detailed data collection
"""

from datetime import datetime
from app.models import db


class Property(db.Model):
    """Property Model with comprehensive data collection - 300+ fields"""
    
    __tablename__ = 'properties'
    
    # ========== BASIC INFORMATION ==========
    id = db.Column(db.Integer, primary_key=True)
    ulpin = db.Column(db.String(50), unique=True, nullable=True, index=True)
    
    # ========== LOCATION DETAILS (15 fields) ==========
    state = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    taluka = db.Column(db.String(100))
    village_city = db.Column(db.String(100), nullable=False)
    locality = db.Column(db.String(200))
    sub_locality = db.Column(db.String(200))
    street_address = db.Column(db.Text)
    landmark = db.Column(db.String(200))
    pincode = db.Column(db.String(10))
    ward_number = db.Column(db.String(50))
    zone = db.Column(db.String(100))
    municipal_area = db.Column(db.Boolean, default=False)
    gram_panchayat = db.Column(db.String(200))
    assembly_constituency = db.Column(db.String(100))
    parliamentary_constituency = db.Column(db.String(100))
    
    # ========== GPS & MAPPING (10 fields) ==========
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    gps_latitude = db.Column(db.Float)
    gps_longitude = db.Column(db.Float)
    altitude = db.Column(db.Float)
    polygon_coordinates = db.Column(db.Text)  # JSON
    property_corners_gps = db.Column(db.Text)  # JSON
    mapping_accuracy = db.Column(db.String(50))
    survey_method = db.Column(db.String(100))
    last_survey_date = db.Column(db.Date)
    
    # ========== LAND MEASUREMENTS (20 fields) ==========
    survey_number = db.Column(db.String(100))
    plot_number = db.Column(db.String(100))
    block_number = db.Column(db.String(100))
    khasra_number = db.Column(db.String(100))
    
    area = db.Column(db.Float, nullable=False)
    area_unit = db.Column(db.Enum('sqm', 'sqft', 'acre', 'hectare', 'gunta', 'bigha', name='area_units'))
    
    length = db.Column(db.Float)
    width = db.Column(db.Float)
    perimeter = db.Column(db.Float)
    
    road_frontage = db.Column(db.Float)
    frontage_direction = db.Column(db.String(50))
    
    plot_shape = db.Column(db.String(50))  # rectangular, irregular, triangular
    slope_percentage = db.Column(db.Float)
    terrain_type = db.Column(db.String(100))  # flat, sloping, hilly
    elevation_from_road = db.Column(db.Float)
    
    built_up_area = db.Column(db.Float)
    carpet_area = db.Column(db.Float)
    super_built_up_area = db.Column(db.Float)
    balcony_area = db.Column(db.Float)
    common_area_share = db.Column(db.Float)
    
    # ========== BOUNDARIES (8 fields) ==========
    north_boundary = db.Column(db.String(200))
    south_boundary = db.Column(db.String(200))
    east_boundary = db.Column(db.String(200))
    west_boundary = db.Column(db.String(200))
    north_boundary_length = db.Column(db.Float)
    south_boundary_length = db.Column(db.Float)
    east_boundary_length = db.Column(db.Float)
    west_boundary_length = db.Column(db.Float)
    
    # ========== PROPERTY CLASSIFICATION (15 fields) ==========
    property_type = db.Column(db.Enum('residential', 'commercial', 'agricultural', 
                                      'industrial', 'institutional', 'mixed_use', name='property_types'))
    sub_property_type = db.Column(db.String(100))  # villa, apartment, farmhouse, etc
    land_category_id = db.Column(db.Integer, db.ForeignKey('land_categories.id'))
    usage_type_id = db.Column(db.Integer, db.ForeignKey('usage_types.id'))
    
    current_land_use = db.Column(db.String(200))
    proposed_land_use = db.Column(db.String(200))
    zoning_classification = db.Column(db.String(100))
    development_zone = db.Column(db.String(100))
    
    is_freehold = db.Column(db.Boolean, default=True)
    lease_type = db.Column(db.String(100))
    lease_years_remaining = db.Column(db.Integer)
    
    property_nature = db.Column(db.String(100))  # urban, rural, semi-urban
    property_age_years = db.Column(db.Integer)
    property_condition = db.Column(db.String(100))  # new, good, average, poor
    occupancy_status = db.Column(db.String(100))  # owner-occupied, tenant, vacant
    
    # ========== CONSTRUCTION DETAILS (25 fields) ==========
    is_constructed = db.Column(db.Boolean, default=False)
    construction_type = db.Column(db.String(100))  # RCC, load-bearing, etc
    construction_quality = db.Column(db.String(100))  # premium, standard, basic
    
    number_of_floors = db.Column(db.Integer)
    floor_number = db.Column(db.Integer)  # for apartments
    total_floors_in_building = db.Column(db.Integer)
    
    number_of_rooms = db.Column(db.Integer)
    number_of_bedrooms = db.Column(db.Integer)
    number_of_bathrooms = db.Column(db.Integer)
    number_of_kitchens = db.Column(db.Integer)
    number_of_balconies = db.Column(db.Integer)
    
    has_basement = db.Column(db.Boolean, default=False)
    basement_area = db.Column(db.Float)
    has_terrace = db.Column(db.Boolean, default=False)
    terrace_area = db.Column(db.Float)
    has_garage = db.Column(db.Boolean, default=False)
    parking_spaces = db.Column(db.Integer)
    
    ceiling_height = db.Column(db.Float)
    flooring_type = db.Column(db.String(200))  # marble, tiles, wooden
    roofing_type = db.Column(db.String(200))  # RCC, asbestos, tile
    wall_type = db.Column(db.String(200))
    doors_windows_type = db.Column(db.String(200))
    
    year_of_construction = db.Column(db.Integer)
    last_renovation_year = db.Column(db.Integer)
    depreciation_percentage = db.Column(db.Float)
    remaining_life_years = db.Column(db.Integer)
    
    # ========== SOIL & AGRICULTURE (15 fields) ==========
    soil_type = db.Column(db.String(100))  # red, black, alluvial, sandy, clayey
    soil_quality = db.Column(db.String(100))  # excellent, good, average, poor
    soil_ph_level = db.Column(db.Float)
    soil_fertility = db.Column(db.String(100))
    soil_depth_cm = db.Column(db.Float)
    
    is_irrigated = db.Column(db.Boolean, default=False)
    irrigation_type = db.Column(db.String(200))  # well, canal, drip, sprinkler
    number_of_crops_per_year = db.Column(db.Integer)
    current_crop = db.Column(db.String(200))
    previous_crops = db.Column(db.Text)  # JSON array
    crop_yield_per_acre = db.Column(db.Float)
    
    has_trees = db.Column(db.Boolean, default=False)
    tree_count = db.Column(db.Integer)
    tree_types = db.Column(db.Text)  # JSON
    
    is_organic_certified = db.Column(db.Boolean, default=False)
    organic_certification_number = db.Column(db.String(100))
    
    # ========== WATER RESOURCES (15 fields) ==========
    water_source = db.Column(db.String(200))  # municipal, borewell, well, river
    has_borewell = db.Column(db.Boolean, default=False)
    borewell_depth_ft = db.Column(db.Float)
    borewell_yield_gpm = db.Column(db.Float)
    water_table_depth_ft = db.Column(db.Float)
    
    has_open_well = db.Column(db.Boolean, default=False)
    well_depth_ft = db.Column(db.Float)
    well_diameter_ft = db.Column(db.Float)
    
    has_water_connection = db.Column(db.Boolean, default=False)
    water_connection_type = db.Column(db.String(100))
    water_meter_number = db.Column(db.String(100))
    water_supply_hours_per_day = db.Column(db.Integer)
    
    water_quality = db.Column(db.String(100))  # potable, non-potable, treated
    water_testing_date = db.Column(db.Date)
    water_storage_capacity_liters = db.Column(db.Integer)
    
    # ========== ELECTRICITY & UTILITIES (12 fields) ==========
    has_electricity = db.Column(db.Boolean, default=False)
    electricity_connection_type = db.Column(db.String(100))  # residential, commercial, industrial
    electricity_load_kw = db.Column(db.Float)
    electricity_meter_number = db.Column(db.String(100))
    electricity_provider = db.Column(db.String(200))
    has_three_phase = db.Column(db.Boolean, default=False)
    
    has_gas_connection = db.Column(db.Boolean, default=False)
    gas_connection_number = db.Column(db.String(100))
    
    has_solar_panels = db.Column(db.Boolean, default=False)
    solar_capacity_kw = db.Column(db.Float)
    
    has_generator = db.Column(db.Boolean, default=False)
    generator_capacity_kva = db.Column(db.Float)
    
    # ========== ROAD & ACCESS (10 fields) ==========
    road_access = db.Column(db.String(100))  # direct, through common path
    road_type = db.Column(db.String(100))  # paved, unpaved, tar, cement
    road_width_ft = db.Column(db.Float)
    road_condition = db.Column(db.String(100))  # excellent, good, average, poor
    
    distance_from_main_road_m = db.Column(db.Float)
    nearest_bus_stop_km = db.Column(db.Float)
    nearest_railway_station_km = db.Column(db.Float)
    nearest_airport_km = db.Column(db.Float)
    
    access_road_ownership = db.Column(db.String(100))  # govt, private, common
    right_of_way_width_ft = db.Column(db.Float)
    
    # ========== INFRASTRUCTURE (15 fields) ==========
    has_drainage = db.Column(db.Boolean, default=False)
    drainage_type = db.Column(db.String(100))  # open, covered, underground
    
    has_sewage_connection = db.Column(db.Boolean, default=False)
    sewage_type = db.Column(db.String(100))  # septic, municipal
    
    has_street_lights = db.Column(db.Boolean, default=False)
    street_light_coverage = db.Column(db.String(100))
    
    has_compound_wall = db.Column(db.Boolean, default=False)
    compound_wall_type = db.Column(db.String(100))
    compound_wall_height_ft = db.Column(db.Float)
    
    has_gate = db.Column(db.Boolean, default=False)
    gate_type = db.Column(db.String(100))  # manual, automatic
    
    has_security = db.Column(db.Boolean, default=False)
    security_type = db.Column(db.String(100))  # guard, cctv, alarm
    
    waste_management_type = db.Column(db.String(100))
    green_coverage_percentage = db.Column(db.Float)
    
    # ========== AMENITIES & SURROUNDINGS (20 fields) ==========
    nearest_school_km = db.Column(db.Float)
    school_names = db.Column(db.Text)  # JSON
    
    nearest_hospital_km = db.Column(db.Float)
    hospital_names = db.Column(db.Text)  # JSON
    
    nearest_market_km = db.Column(db.Float)
    nearest_bank_km = db.Column(db.Float)
    nearest_atm_km = db.Column(db.Float)
    nearest_post_office_km = db.Column(db.Float)
    nearest_police_station_km = db.Column(db.Float)
    
    nearest_temple_km = db.Column(db.Float)
    nearest_mosque_km = db.Column(db.Float)
    nearest_church_km = db.Column(db.Float)
    
    nearest_park_km = db.Column(db.Float)
    nearest_playground_km = db.Column(db.Float)
    
    connectivity_rating = db.Column(db.Integer)  # 1-10
    locality_rating = db.Column(db.Integer)  # 1-10
    
    nearby_amenities = db.Column(db.Text)  # JSON list
    nearby_nuisances = db.Column(db.Text)  # pollution, noise, etc
    
    neighborhood_type = db.Column(db.String(100))  # posh, middle-class, developing
    future_development_potential = db.Column(db.Text)
    
    # ========== ENVIRONMENTAL (10 fields) ==========
    flood_zone = db.Column(db.Boolean, default=False)
    flood_history = db.Column(db.Text)
    
    earthquake_zone = db.Column(db.String(50))  # Zone I-V
    cyclone_prone = db.Column(db.Boolean, default=False)
    
    pollution_level = db.Column(db.String(100))  # low, medium, high
    noise_level = db.Column(db.String(100))
    
    has_water_body_nearby = db.Column(db.Boolean, default=False)
    water_body_type = db.Column(db.String(100))  # river, lake, pond
    water_body_distance_m = db.Column(db.Float)
    
    air_quality_index = db.Column(db.Integer)
    
    # ========== LEGAL & DOCUMENTATION (20 fields) ==========
    deed_number = db.Column(db.String(100))
    deed_type = db.Column(db.String(100))  # sale, gift, inheritance
    deed_date = db.Column(db.Date)
    
    registration_number = db.Column(db.String(100))
    registration_office = db.Column(db.String(200))
    sro_location = db.Column(db.String(200))  # Sub-Registrar Office
    
    document_7_12 = db.Column(db.String(100))  # Maharashtra specific
    document_8_a = db.Column(db.String(100))
    property_card_number = db.Column(db.String(100))
    
    has_clear_title = db.Column(db.Boolean, default=True)
    title_verification_date = db.Column(db.Date)
    title_verification_report = db.Column(db.String(500))
    
    has_encumbrance = db.Column(db.Boolean, default=False)
    encumbrance_details = db.Column(db.Text)
    encumbrance_certificate_date = db.Column(db.Date)
    
    mutation_status = db.Column(db.String(100))  # pending, completed
    mutation_certificate_number = db.Column(db.String(100))
    
    legal_disputes = db.Column(db.Text)
    court_cases = db.Column(db.Text)  # JSON
    legal_heirs_count = db.Column(db.Integer)
    
    # ========== PLANNING & APPROVALS (15 fields) ==========
    building_plan_approved = db.Column(db.Boolean, default=False)
    building_plan_number = db.Column(db.String(100))
    building_plan_approval_date = db.Column(db.Date)
    approving_authority = db.Column(db.String(200))
    
    occupancy_certificate = db.Column(db.String(100))
    occupancy_certificate_date = db.Column(db.Date)
    
    commencement_certificate = db.Column(db.String(100))
    completion_certificate = db.Column(db.String(100))
    
    fsi_far = db.Column(db.Float)  # Floor Space Index / Floor Area Ratio
    ground_coverage = db.Column(db.Float)
    permissible_fsi = db.Column(db.Float)
    utilized_fsi = db.Column(db.Float)
    
    development_agreement = db.Column(db.String(500))
    rera_registration = db.Column(db.String(100))
    rera_approval_date = db.Column(db.Date)
    
    # ========== VALUATION (15 fields) ==========
    market_value = db.Column(db.Float)
    registered_value = db.Column(db.Float)
    govt_guidance_value = db.Column(db.Float)
    stamp_duty_paid = db.Column(db.Float)
    registration_charges_paid = db.Column(db.Float)
    
    last_transaction_value = db.Column(db.Float)
    last_transaction_date = db.Column(db.Date)
    
    current_rental_value = db.Column(db.Float)
    expected_rental_yield = db.Column(db.Float)
    
    appreciation_rate_annual = db.Column(db.Float)
    depreciation_value = db.Column(db.Float)
    
    property_tax_annual = db.Column(db.Float)
    maintenance_charges_annual = db.Column(db.Float)
    
    insurance_value = db.Column(db.Float)
    insurance_policy_number = db.Column(db.String(100))
    
    # ========== PREVIOUS OWNERSHIP (10 fields) ==========
    previous_owner_name = db.Column(db.String(200))
    previous_owner_relationship = db.Column(db.String(100))  # father, seller, etc
    purchase_date = db.Column(db.Date)
    purchase_price = db.Column(db.Float)
    
    ownership_duration_years = db.Column(db.Integer)
    ownership_chain = db.Column(db.Text)  # JSON - history
    
    inheritance_details = db.Column(db.Text)
    gift_deed_details = db.Column(db.Text)
    exchange_details = db.Column(db.Text)
    partition_details = db.Column(db.Text)
    
    # ========== PHOTOS & MEDIA (5 fields) ==========
    featured_image = db.Column(db.String(500))
    property_images = db.Column(db.Text)  # JSON array
    property_videos = db.Column(db.Text)  # JSON array
    drone_images = db.Column(db.Text)  # JSON array
    documents_scanned = db.Column(db.Text)  # JSON array
    
    # ========== STATUS & WORKFLOW (10 fields) ==========
    status = db.Column(db.Enum('pending', 'under_review', 'documents_verified', 
                              'approved', 'rejected', 'active', 'disputed', 'frozen',
                              name='property_status'), default='pending', index=True)
    
    registration_date = db.Column(db.DateTime)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approval_date = db.Column(db.DateTime)
    rejection_reason = db.Column(db.Text)
    
    verification_level = db.Column(db.Integer, default=0)  # 0-5
    verification_notes = db.Column(db.Text)
    
    is_disputed = db.Column(db.Boolean, default=False)
    is_mortgaged = db.Column(db.Boolean, default=False)
    is_rented = db.Column(db.Boolean, default=False)
    
    # ========== ADDITIONAL INFORMATION (5 fields) ==========
    description = db.Column(db.Text)
    remarks = db.Column(db.Text)
    special_features = db.Column(db.Text)  # JSON
    advantages = db.Column(db.Text)
    disadvantages = db.Column(db.Text)
    
    # ========== TIMESTAMPS (2 fields) ==========
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ========== RELATIONSHIPS ==========
    land_category = db.relationship('LandCategory', backref='properties')
    usage_type = db.relationship('UsageType', backref='properties')
    approved_by_user = db.relationship('User', foreign_keys=[approved_by])
    
    ownerships = db.relationship('Ownership', back_populates='property', cascade='all, delete-orphan', lazy='dynamic')
    documents = db.relationship('Document', back_populates='property', cascade='all, delete-orphan', lazy='dynamic')
    mutations = db.relationship('Mutation', back_populates='property', cascade='all, delete-orphan', lazy='dynamic')
    tax_assessments = db.relationship('TaxAssessment', back_populates='property', cascade='all, delete-orphan', lazy='dynamic')
    payments = db.relationship('Payment', back_populates='property', lazy='dynamic')
    valuations = db.relationship('PropertyValuation', back_populates='property', cascade='all, delete-orphan', lazy='dynamic')
    inspections = db.relationship('PropertyInspection', back_populates='property', cascade='all, delete-orphan', lazy='dynamic')
    disputes = db.relationship('PropertyDispute', back_populates='property', cascade='all, delete-orphan', lazy='dynamic')
    mortgages = db.relationship('PropertyMortgage', back_populates='property', cascade='all, delete-orphan', lazy='dynamic')
    
    def generate_ulpin(self):
        if self.ulpin:
            return self.ulpin
        state_code = self.state[:2].upper() if self.state else 'XX'
        district_code = self.district[:3].upper() if self.district else 'XXX'
        village_code = self.village_city[:3].upper() if self.village_city else 'XXX'
        year = datetime.utcnow().year
        self.ulpin = f"{state_code}{district_code}{village_code}{year}{self.id:06d}"
        return self.ulpin
    
    def get_current_owners(self):
        return [ownership.owner for ownership in self.ownerships.filter_by(is_active=True).all()]
    
    def get_total_ownership_percentage(self):
        return sum([ownership.ownership_percentage for ownership in self.ownerships.filter_by(is_active=True).all()])
    
    def __repr__(self):
        return f'<Property {self.ulpin or self.id} - {self.village_city}>'
