app_name = "krcs_surge"
app_title = "KRCS Surge System"
app_publisher = "KRCS"
app_description = "OneRC - VMMS"
app_email = "admin@redcross.or.ke"
app_license = "MIT"

# Includes in <head>
app_include_css = ["/assets/krcs_surge/css/leaflet.css"]
app_include_js = ["/assets/krcs_surge/js/leaflet.js"]

web_include_css = ["/assets/krcs_surge/css/leaflet.css"]
web_include_js = ["/assets/krcs_surge/js/leaflet.js"]

# Events
doc_events = {
    "LMS Certificate": {
        "after_insert": "krcs_surge.integrations.lms_sync.on_certificate_issued"
    },
    "Company": {
        "after_insert": "krcs_surge.integrations.setup_ops.create_branch_warehouse"
    }
}

# Permissions
has_permission = {
    "Project": "krcs_surge.permissions.check_project_permission",
    "Event": "krcs_surge.permissions.check_event_permission"
}

# Scheduler
scheduler_events = {
    "hourly": [
        "krcs_surge.integrations.navision_sync.sync_stock_levels"
    ]
}

# Portal Menu
portal_menu_items = [
    {"title": "My Dashboard", "route": "/volunteer-dashboard", "role": "Volunteer"},
    {"title": "Open Opportunities", "route": "/volunteer-opportunities", "role": "Volunteer"},
    {"title": "My Training", "route": "/lms", "role": "Volunteer"},
    {"title": "My Certificates", "route": "/volunteer-certificates", "role": "Volunteer"}
]