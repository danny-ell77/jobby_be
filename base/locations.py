from django.db import models


class NigeriaStates(models.TextChoices):
    ABIA = "AB", "Abia"
    ADAMAWA = "AD", "Adamawa"
    AKWA_IBOM = "AK", "Akwa Ibom"
    ANAMBRA = "AN", "Anambra"
    BAUCHI = "BA", "Bauchi"
    BAYELSA = "BY", "Bayelsa"
    BENUE = "BE", "Benue"
    BORNO = "BO", "Borno"
    CROSS_RIVER = "CR", "Cross River"
    DELTA = "DE", "Delta"
    EBONYI = "EB", "Ebonyi"
    EDO = "ED", "Edo"
    EKITI = "EK", "Ekiti"
    ENUGU = "EN", "Enugu"
    GOMBE = "GO", "Gombe"
    IMO = "IM", "Imo"
    JIGAWA = "JI", "Jigawa"
    KADUNA = "KD", "Kaduna"
    KANO = "KN", "Kano"
    KATSINA = "KT", "Katsina"
    KEBBI = "KE", "Kebbi"
    KOGI = "KO", "Kogi"
    KWARA = "KW", "Kwara"
    LAGOS = "LA", "Lagos"
    NASARAWA = "NA", "Nasarawa"
    NIGER = "NI", "Niger"
    OGUN = "OG", "Ogun"
    ONDO = "ON", "Ondo"
    OSUN = "OS", "Osun"
    OYO = "OY", "Oyo"
    PLATEAU = "PL", "Plateau"
    RIVERS = "RI", "Rivers"
    SOKOTO = "SO", "Sokoto"
    TARABA = "TA", "Taraba"
    YOBE = "YO", "Yobe"
    ZAMFARA = "ZA", "Zamfara"
    FCT = "FC", "Federal Capital Territory"
