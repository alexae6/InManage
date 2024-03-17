from django.shortcuts import  render, redirect
from .forms import NewUserForm, ChangePatient
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import math
from .models import Patient
from django.db.models import Count
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
	accepted = Patient.objects.filter(Status__contains="accepted").count()
	cms_yes = Patient.objects.filter(CMS__contains="yes").count()
	patients = Patient.objects.all()
	patients_count = Patient.objects.all().count()
	hold1 = (cms_yes)/(patients_count)*100
	cms_percent = math.ceil(hold1*100)/100

	accepted = Patient.objects.filter(Status__contains="accepted").count()
	rejected = Patient.objects.filter(Status__contains="rejected").count()
	pending = patients_count-(accepted+rejected)

	return render(request,"home.html",{"accepted":accepted,"cms_percent":cms_percent,"patients":patients,"rejected":rejected,"pending":pending})

def searchpatient(request):
	if request.method == "POST":
		form = ChangePatient(request.POST)
		if form.is_valid(): 
			form.save()
			return redirect("base:searchpatient")
	form = ChangePatient()
	return render(request, "patientinfo.html",{"form":form})
	
def patientinfo(request,entry):
	patient = Patient.objects.get(patientname=entry)
	form = ChangePatient(request.POST, instance=patient)
	if request.method == "POST":
		if form.is_valid():
			form.save()
			return render(request,"patientinfo.html",{"patient":patient})
	return render(request, "patientinfo.html",{"patient":patient,"form":form})
    
def upload(request):
    if request.method == 'POST' and request.FILES['patientfile'] and 'runscript' in request.POST:
        from pdf_processor import main
        from import_data import run
        import threading
        patientfile = request.FILES['patientfile']
        fs = FileSystemStorage()
        filename = fs.save(patientfile.name, patientfile)
        uploaded_file_url = fs.url(filename)
        t1 = threading.Thread(target = main, args = (['pdf_processor.py', '-i', 'patientfile'],))
        t1.start()
        run()
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    #if request.method == 'POST' and 'runscript' in request.POST:
    #    from pdf_processor import main
    #    from import_data import run
    #    main('pdf_processor.py', '-i', 'patientfile')
    #    run()
    #   return render(request, "upload.html")  
    
    messages.info(request, 'Your patient record has been uploaded successfully!')
    return render(request, "upload.html")


def monthly(request):
	insur_anthem = Patient.objects.filter(insurancename1="Anthem").count()
	insur_UHC = Patient.objects.filter(insurancename1="UHC").count()
	insur_medicaid = Patient.objects.filter(insurancename1="Medicaid").count()
	insur_blue = Patient.objects.filter(insurancename1="Blue Cross").count()
	insur_total = Patient.objects.all().count()
	insur_other = insur_total-(insur_anthem+insur_UHC+insur_medicaid+insur_blue)

	
	cms_yes = Patient.objects.filter(CMS__contains="yes").count()
	patients = Patient.objects.all().count()
	hold1 = (cms_yes)/(patients)*100
	cms_percent = math.ceil(hold1*100)/100

	accepted = Patient.objects.filter(Status__contains="accepted").count()
	rejected = Patient.objects.filter(Status__contains="rejected").count()
	pending = patients-(accepted+rejected)
	hold2 = accepted/patients*100
	bed_percent = math.ceil(hold2*100)/100

	hospitalIUr = Patient.objects.filter(ReferringHospital = "IU Health Arnett Hospital").filter(Status="rejected").count()
	hospitalIUa = Patient.objects.filter(ReferringHospital = "IU Health Arnett Hospital").filter(Status="accepted").count()
	hospitalIUc = Patient.objects.filter(ReferringHospital = "IU Health Arnett Hospital").filter(CMS="yes").count()
	FranEastr = Patient.objects.filter(ReferringHospital = "Franscisican Health Lafayette East").filter(Status="rejected").count()
	FranEasta = Patient.objects.filter(ReferringHospital = "Franscisican Health Lafayette East").filter(Status="accepted").count()
	FranEastc = Patient.objects.filter(ReferringHospital = "Franscisican Health Lafayette East").filter(CMS="yes").count()
	FranCentralr = Patient.objects.filter(ReferringHospital = "Franscisican Health Lafayette Central").filter(Status="rejected").count()
	FranCentrala = Patient.objects.filter(ReferringHospital = "Franscisican Health Lafayette Central").filter(Status="accepted").count()
	FranCentralc = Patient.objects.filter(ReferringHospital = "Franscisican Health Lafayette Central").filter(CMS="yes").count()
	other_refr = rejected - (hospitalIUr+FranEastr+FranCentralr)
	other_refa = accepted - (hospitalIUa+FranEasta+FranCentrala)
	other_refc = cms_yes - (hospitalIUc+FranEastc+FranCentralc)
	
	#reason = Patient.objects.values('Rejectiondis').annotate(dcount=Count('Rejectiondis'))

	reason1 = Patient.objects.filter(Rejectiondis__contains='CMS').count()
	reason2 = Patient.objects.filter(Rejectiondis__contains='Insurance').count()
	reason3 = Patient.objects.filter(Rejectiondis__contains='qualif').count()
	reasonother = rejected-(reason1+reason2+reason3)


	return render(request,"monthly.html",{"insur_anthem":insur_anthem,"insur_UHC":insur_UHC,"insur_medicaid":insur_medicaid,"insur_blue":insur_blue,"insur_other":insur_other,
	"cms_percent":cms_percent,"bed_percent":bed_percent,"accepted":accepted,"rejected":rejected,"pending":pending,
	"hospitalIUr":hospitalIUr,"hospitalIUa":hospitalIUa,"hospitalIUc":hospitalIUc,"FranEastr":FranEastr,"FranEasta":FranEasta,"FranEastc":FranEastc,"FranCentralr":FranCentralr,"FranCentrala":FranCentrala,"FranCentralc":FranCentralc,"other_refr":other_refr,"other_refa":other_refa,"other_refc":other_refc,
	"reason1":reason1,"reason2":reason2,"reason3":reason3,"reasonother" :reasonother})

def calendar(request):
    return render(request, "calendar.html")

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("base:home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="base/register.html", context={"register_form":form})    

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("base:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request=request, template_name="base/login.html", context={"login_form": form})

# def login_request(request):
# 	if request.method == "POST":
# 		form = AuthenticationForm(request, data=request.POST)
# 		if form.is_valid():
# 			username = form.cleaned_data.get('username')
# 			password = form.cleaned_data.get('password')
# 			user = authenticate(username=username, password=password)
# 			if user is not None:
# 				login(request, user)
# 				messages.info(request, f"You are now logged in as {username}.")
# 				return redirect("base:home")
# 			else:
# 				messages.error(request,"Invalid username or password.")
# 		else:
# 			messages.error(request,"Invalid username or password.")
# 	form = AuthenticationForm()
# 	return render(request=request, template_name="base/login.html", context={"login_form":form})
