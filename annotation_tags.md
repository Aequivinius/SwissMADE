ANNOTATION TAGS

my abbreviations
iddr, dr for drugs
p and idp procedures
d and idd diagnosis
idm for medication_order
idt for transfer

and lint all of them

useful document: https://www.medizin.uni-halle.de/fileadmin/Bereichsordner/Kliniken/HerzThoraxchirurgie/Studenten/h%C3%A4ufige_Abk%C3%BCrzungen_Herzchirurgie.pdf
lateron: counts per entity, list of drug forms

it probably would have been better to annotate <date> and give the same id

maybe to gather fecit tag for procedures is not so smart

change abbreviations
write dtd and check

-> change dates
-> don't annotate fecit anymore

changed : if anonymisation didn't go well, eg RCHIHERB3

report_date

GENERAL ADMINISTRATIVE DATA
age (because DOB is not always directly mentioned)


CLINICAL MEASUREMENTS
height
weight  (since this can change, might make sense to try and capture date)
bloodpressure

(we do not track BMI, though this is easily calculated from height and weight)

PATIENT LOCATIONS & TRANSFERS
unit_hospizalization : not sure if this is 'Herz- und Gefässchirurgie' or 'Bettenstation' (as in RCHIHERAB3_1). So far annotated all these like this.
admission
discharge
transfer (with attributes date, from, to, name,  - eg stationäre Rehabilitation nach Mammern, suggested_duration)

DIAGNOSES & PROCEDURES
diagnosis : this is not in the protocole, somehow, but it seems stupid not to extract  it. I presume these are later then to be mapped to DRGs codes (diagnosis related group)
> it's not so easy to distinguish between symptom and diagnosis
diagnosis_text : this might make sense to also extract it, but it contains lots of abbreviations and vernacular that a layperson doesn't understand. This is why I didn't annotate it. 
attributes such as degree (leichte Mitralinsuffizienz), negated, suspected

procedure : In there, there are mentions of different procedures, which I tried to annotate as good as possible (given I don't have any expert knowledge). These can then later be mapped to CHOP codes
> these are often paired with a date and sometimes a place, which should also be extracted, but in this run of annotation I didn't do it (for example: '<procedure>MRI</procedure> Münsterlingen 10.07.2014' in RCHIHERAB3_1)
they can have attributes : date, location, fecit, indicated, unsuccessful

drugs : with attributes dosage, ingredient / brand name

LABORATORY VALUES | OTHER
oxygen_saturation

blood_pressure

these are tricky, because I need to translate stuff:


Thrombozyten -> platelets
erythrozyten -> red_blood_cells
Leukozyten -> white_blood_cells
I guess PTT is pt
natrium -> sodium
Kalium -> potassium
Harnstoff -> urea
crp

they can also have type positive_ negative_change

MEDICATION ORDER
main tag goes onto drug, has duration tag, until
maybe also reason

start date                   <    discharge 
                   admission         <        discontinuation