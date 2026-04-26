from django.contrib import admin
from .models import User, PharmacyProfile, Antibiotic, SaleRecord, Prescription, SystemSettings


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        ('Basic Information', {'fields': ('username', 'email', 'first_name', 'last_name')}),
        ('Role & Location', {'fields': ('role', 'latitude', 'longitude')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('date_joined', 'last_login')}),
    )


@admin.register(PharmacyProfile)
class PharmacyProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'user', 'latitude', 'longitude')
    list_filter = ('name',)
    search_fields = ('name', 'address', 'user__username')
    readonly_fields = ('latitude', 'longitude')


@admin.register(Antibiotic)
class AntibioticAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'category')
    list_filter = ('group', 'category')
    search_fields = ('name', 'group', 'category')
    ordering = ('name',)


@admin.register(SaleRecord)
class SaleRecordAdmin(admin.ModelAdmin):
    list_display = ('antibiotic', 'pharmacy', 'quantity', 'patient_age', 'patient_gender', 'timestamp')
    list_filter = ('timestamp', 'patient_gender', 'pharmacy', 'antibiotic__group')
    search_fields = ('pharmacy__name', 'antibiotic__name', 'doctor_name', 'prescription_reference')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    fieldsets = (
        ('Sale Information', {'fields': ('pharmacy', 'antibiotic', 'quantity')}),
        ('Patient Details', {'fields': ('patient_age', 'patient_gender')}),
        ('Prescription Reference', {'fields': ('doctor_name', 'prescription_reference')}),
        ('Timestamp', {'fields': ('timestamp',)}),
    )


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'antibiotic', 'dosage', 'frequency', 'duration_days', 'date')
    list_filter = ('date', 'antibiotic__group', 'user')
    search_fields = ('user__username', 'antibiotic__name')
    readonly_fields = ('date',)
    date_hierarchy = 'date'
    fieldsets = (
        ('User & Antibiotic', {'fields': ('user', 'antibiotic')}),
        ('Dosage Information', {'fields': ('dosage', 'frequency', 'duration_days')}),
        ('Date', {'fields': ('date',)}),
    )


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('low_risk_limit', 'moderate_risk_limit', 'high_risk_limit')
    fieldsets = (
        ('Risk Thresholds', {'fields': ('low_risk_limit', 'moderate_risk_limit', 'high_risk_limit')}),
    )
    
    def has_add_permission(self, request):
        # Allow only one SystemSettings instance
        return not SystemSettings.objects.exists()
