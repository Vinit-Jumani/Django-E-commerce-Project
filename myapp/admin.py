from django.contrib import admin
from .models import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table,TableStyle

# Register your models here.

def exportto_pdf(self, request, queryset):
    # Create a new PDF
    model_name = self.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment;filename={model_name}.pdf'
    # Generate the report using ReportLab
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    # Define the style for the table
    style = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 14),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    # Create the table headers
    headers = ['User_name','Email_id', 'Phone_no','Password','Role','Status']
    # Create the table data
    data = []
    for obj in queryset:
        data.append([obj.User_name,obj.Email_id, obj.Phone_no,obj.Password,obj.Role,obj.Status])
    # Create the table
    t = Table([headers] + data, style=style)
    # Add the table to the elements array
    elements.append(t)
    # Build the PDF document
    doc.build(elements)
    return response
exportto_pdf.short_description = "Export to PDF"
class Show_Login_Table(admin.ModelAdmin):
    list_display = ["id","User_name","Email_id","Phone_no","Password","Role","Status"]
    actions = [exportto_pdf]
admin.site.register(Login_Table,Show_Login_Table)

class  Show_Detail_Table(admin.ModelAdmin):
    list_display = ["login_id","name","DOB","gender","user_dp"]
admin.site.register(Detail_Table,Show_Detail_Table)

class Show_Category_Table(admin.ModelAdmin):
    list_display = ["Category_Name"]
admin.site.register(Category_Table,Show_Category_Table)

def export_to_pdf(self, request, queryset):
    # Create a new PDF
    model_name = self.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment;filename={model_name}.pdf'
    # Generate the report using ReportLab
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    # Define the style for the table
    style = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 14),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    # Create the table headers
    # headers = [field.verbose_name for field in self.model.fields]
    headers = ["Category_id","Vendor","Product_Name","Product_Price","Stock","Product_Status"]
    # Create the table data
    data = []
    for obj in queryset:
        # data_row = [str(getattr(obj, field.name)) for feild in self.model._meta.fields]
        data.append([obj.Category_id, obj.Vendor,obj.Product_Name,obj.Product_Price,obj.Stock,obj.Product_Status])
    # Create the table
    t = Table([headers] + data, style=style)
    # Add the table to the elements array
    elements.append(t)
    # Build the PDF document
    doc.build(elements)
    return response
    export_to_pdf.short_description = "Export to PDF"


class Show_Product_Table(admin.ModelAdmin):
    list_display = ["Category_id","Vendor","Product_Name","short_description","Product_Price","Stock","product_image","product_image1","product_image2","product_image3","Product_Status"]
    actions = [export_to_pdf]
    def short_description(self, obj):
        return obj.Product_Description[:20] + '...' if len(obj.Product_Description) > 20 else obj.Product_Description
    short_description.short_description = 'Product Description'
    actions = [export_to_pdf]
admin.site.register(Product_Table,Show_Product_Table)


class Show_Cart_Table(admin.ModelAdmin):
    list_display = ["Login_ID","Product_ID","Price","Total_Amount", "Quantity","Order_status"]
admin.site.register(Cart_Table,Show_Cart_Table)

def exporttopdf(self, request, queryset):
    # Create a new PDF
    model_name = self.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment;filename={model_name}.pdf'
    # Generate the report using ReportLab
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    # Define the style for the table
    style = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 14),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    # Create the table headers
    # headers = [field.verbose_name for field in self.model.fields]
    headers = ["Login_ID","totalAmount","Address","order_status","Payment_status"]
    # Create the table data
    data = []
    for obj in queryset:
        # data_row = [str(getattr(obj, field.name)) for feild in self.model._meta.fields]
        data.append([obj.Login_ID, obj.totalAmount,obj.Address,obj.order_status,obj.Payment_status])
    # Create the table
    t = Table([headers] + data, style=style)
    # Add the table to the elements array
    elements.append(t)
    # Build the PDF document
    doc.build(elements)
    return response
exporttopdf.short_description = "Export to PDF"
class Show_Order_Table(admin.ModelAdmin):
    list_display = ["Login_ID","totalAmount","Address","order_status","Payment_status"]
    actions = [exporttopdf]
admin.site.register(product_order,Show_Order_Table)

def export_topdf(self, request, queryset):
    # Create a new PDF
    model_name = self.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment;filename={model_name}.pdf'
    # Generate the report using ReportLab
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    # Define the style for the table
    style = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 14),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    # Create the table headers
    # headers = [field.verbose_name for field in self.model.fields]
    headers = ["Login_ID","amount","payment_method","transaction_id","payment_status"]
    # Create the table data
    data = []
    for obj in queryset:
        # data_row = [str(getattr(obj, field.name)) for feild in self.model._meta.fields]
        data.append([obj.Login_ID,obj.amount,obj.payment_method,obj.transaction_id,obj.payment_status])
    # Create the table
    t = Table([headers] + data, style=style)
    # Add the table to the elements array
    elements.append(t)
    # Build the PDF document
    doc.build(elements)
    return response
export_topdf.short_description = "Export to PDF"
class Show_Payment_Table(admin.ModelAdmin):
    list_display = ["Login_ID","order_id","amount","payment_method","transaction_id","payment_status"]
    actions = [export_topdf]
admin.site.register(Payment_Table,Show_Payment_Table)
class Show_Card_Table(admin.ModelAdmin):
    list_display = ["name","card_number","card_cvv","exp_date","card_balance"]
admin.site.register(CardDetail,Show_Card_Table)

class Show_Feedback_Table(admin.ModelAdmin):
    list_display = ["Login_ID","order_id","ratings","comment"]
admin.site.register(Feedback_Table,Show_Feedback_Table)

class Show_Complain_Table(admin.ModelAdmin):
    list_display = ["Loging_id","complain","Complain_Datetime","Complain_Status"]
admin.site.register(Complain_Table,Show_Complain_Table)

class Show_Contact_Us_Table(admin.ModelAdmin):
    list_display = ["First_name","Last_name","Email_ID","Phone_No","Message","Timestamp"]
admin.site.register(Contact_Us_Table,Show_Contact_Us_Table)

