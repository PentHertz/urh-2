# URH Auto-Decoder: Supported Protocols

**Total: 327 protocols** from rtl_433 + Flipper-ARF automotive databases.

## Decoders Available

| Decoder | Raw Pattern | Used By |
|---------|-------------|---------|
| NRZ (No encoding) | Passthrough | OOK_PCM, FSK_PCM, OOK_PPM |
| NRZ + Invert | 0→1, 1→0 | Inverted signals |
| Manchester I (IEEE) | 01→1, 10→0 | Weather sensors, ERT meters |
| Manchester II (Thomas) | 10→1, 01→0 | Opposite convention |
| Differential Manchester | Transition=1, No transition=0 | Ford keys, Funkbus |
| PWM (Short=1, Long=0) | 100→1, 110→0 | HCS200/300, KeeLoq, Acurite |
| PWM (Short=0, Long=1) | 100→0, 110→1 | Inverted PWM |
| Miller | Mid-bit transition=1, same=0 | RFID ISO 14443, EPC Gen2 |

## Modulation Coverage

| Modulation | Protocols | URH Decoder |
|------------|-----------|-------------|
| FSK/PCM | 101 | NRZ |
| OOK/PWM | 83 | PWM |
| OOK/PPM | 61 | NRZ |
| OOK/MANCHESTER_ZEROBIT | 32 | Manchester I/II |
| OOK/PCM | 20 | NRZ |
| FSK/PWM | 7 | PWM |
| FSK/MANCHESTER_ZEROBIT | 6 | Manchester I/II |
| OOK/DMC | 6 | Differential Manchester |
| OOK/RZ | 3 | NRZ |
| OOK/PIWM_DC | 2 | NRZ |
| OOK/NRZS | 1 | NRZ |
| OOK/PWM_OSV1 | 1 | PWM |

## Automotive Key Fobs (16)

| Protocol | Modulation | Bits | Checksum |
|----------|------------|------|----------|
| Fiat Marelli car key | MANCHESTER | 80 | — |
| Fiat SPA platform car key | MANCHESTER | 64 | — |
| Ford Car Key | DMC | 78 | — |
| Ford V0 car key fob | MANCHESTER | 64 | crc8 |
| Honda Car Key | FSK/PWM | 394 | — |
| KIA V0 car key | PWM | 61 | crc8 |
| KIA V1 car key (Manchester) | MANCHESTER | 57 | crc4 |
| KIA V5 car key (mixer cipher) | MANCHESTER | 64 | crc3 |
| KIA V6 car key (AES) | MANCHESTER | 144 | crc8 |
| Mazda Siemens car key | PWM | 64 | parity |
| Mitsubishi V0 car key | PWM | 80 | xor_bytes |
| PSA Peugeot Citroen car key | PWM | 128 | — |
| Porsche Cayenne key fob | PWM | 64 | — |
| Subaru car key fob | PWM | 64 | — |
| Suzuki car key fob | PWM | 64 | crc8 |
| VAG VW Audi Group car key | MANCHESTER | 80 | — |

## Gate & Garage Remotes (19)

| Protocol | Modulation | Bits | Checksum |
|----------|------------|------|----------|
| CAME Atomo rolling code | MANCHESTER | 62 | — |
| CAME Twee | MANCHESTER | 54 | xor_bytes |
| CAME gate remote | PWM | 12 | — |
| Chamberlain CWPIRC PIR Sensor | FSK/PCM | — | crc16 |
| Chamberlain garage door opener | PWM | 10 | — |
| FAAC SLH gate remote (KeeLoq) | PWM | 64 | keeloq |
| Gate TX generic remote | PWM | 24 | — |
| Hormann HSM gate/garage remote | PWM | 44 | — |
| Linear DIP switch garage remote | PWM | 10 | — |
| Linear Megacode Garage/Gate Remotes | PCM | 144 | — |
| NICE Flo gate remote | PWM | 12 | — |
| NICE Flor-S rolling code | PWM | 52 | — |
| Nice Flor-s remote control for gates | PWM | 72 | — |
| Security+ (Keyfob) | PCM | 130 | — |
| Security+ 2.0 (Keyfob) | PCM | 110 | — |
| Security+ V1 Liftmaster/Chamberlain | PWM | 42 | — |
| Security+ V2 Liftmaster/Chamberlain | MANCHESTER | 62 | — |
| Somfy Keytis gate remote | MANCHESTER | 80 | — |
| Somfy Telis blinds/gate remote | MANCHESTER | 56 | — |

## Rolling Code Systems (3)

| Protocol | Modulation | Bits | Checksum |
|----------|------------|------|----------|
| KeeLoq Rolling Code (generic) | PWM | 64 | keeloq |
| Microchip HCS200/HCS300 KeeLoq Hopping Encoder based remotes | PWM | 66 | — |
| Microchip HCS200/HCS300 KeeLoq Hopping Encoder based remotes (FSK) | FSK/PWM | 66 | — |

## Weather Stations & Sensors (51)

| Protocol | Modulation | Bits | Checksum |
|----------|------------|------|----------|
| AOK Weather Station rebrand Holman Industries iWeather WS5029, Conrad AOK-5056, Optex 990018 | FSK/PCM | 96 | lfsr_digest8_reflect,xor_bytes |
| Acurite 592TXR temp/humidity, 592TX temp, 5n1, 3n1, Atlas weather station, 515 fridge/freezer, 6045 lightning, 899 rain, 1190/1192 leak | PWM | 88 | add_bytes,crc16lsb,crc8le,lfsr_digest8,parity_bytes |
| Acurite 896 Rain Gauge | PPM | 88 | add_bytes,crc16lsb,crc8le,lfsr_digest8,parity_bytes |
| AlectoV1 Weather Sensor (Alecto WS3500 WS4500 Ventus W155/W044 Oregon) | PPM | — | — |
| Ambient Weather F007TH, TFA 30.3208.02, SwitchDocLabs F016TH temperature sensor | MANCHESTER | 48 | lfsr_digest8 |
| Ambient Weather TX-8300 Temperature/Humidity Sensor | PPM | — | — |
| Ambient Weather WH31E Thermo-Hygrometer Sensor, EcoWitt WH40 rain gauge, WS68 weather station | FSK/PCM | 144 | add_bytes,crc8 |
| Ambient Weather WH31L (FineOffset WH57) Lightning-Strike sensor | FSK/PCM | 72 | add_bytes,crc8 |
| Auriol 4-LD5661/4-LD5972/4-LD6313 temperature/rain sensors | PPM | 52 | — |
| Baldr / RainPoint rain gauge. | PPM | 37 | — |
| Biltema rain gauge | PPM | — | — |
| Bresser Weather Center 5-in-1 | FSK/PCM | 440 | — |
| Bresser Weather Center 6-in-1, 7-in-1 indoor, soil, new 5-in-1, 3-in-1 wind gauge, Froggit WH6000, Ventus C8488A | FSK/PCM | 440 | add_bytes,lfsr_digest16 |
| Bresser Weather Center 7-in-1, Air Quality PM2.5/PM10 7009970, CO2 7009977, HCHO/VOC 7009978 sensors | FSK/PCM | 240 | lfsr_digest16 |
| Cotech 36-7959, SwitchDocLabs FT020T wireless weather station with USB | MANCHESTER | 112 | crc8 |
| Digitech XC-0324 / AmbientWeather FT005TH temp/hum sensor | PPM | 148 | xor_bytes |
| EMOS E6016 rain gauge | PWM | 73 | add_bytes |
| EMOS E6016 weatherstation with DCF77 | PWM | 120 | add_bytes |
| Emax W6, rebrand Altronics x7063/4/x7064A, Optex 990040/50/51, Orium 13093/13123, Infactory FWS-1200, Newentor Q9, Otio 810025, Protmex PT3390A, Jula Marquant 014331/32, TechniSat IMETEO X6 76-4924-00, Weather Station or temperature/humidity sensor | FSK/PCM | 264 | add_bytes |
| Fine Offset Electronics WH1080/WH3080 Weather Station | PWM | 100 | crc8 |
| Fine Offset Electronics WH1080/WH3080 Weather Station (FSK) | FSK/PCM | 100 | crc8 |
| Fine Offset Electronics WS80 weather station | FSK/PCM | 240 | add_bytes,crc8 |
| Fine Offset Electronics WS85 weather station | FSK/PCM | 500 | add_bytes,crc8 |
| Fine Offset Electronics WS90 weather station | FSK/PCM | 500 | add_bytes,crc8 |
| Fine Offset Electronics, WH0530 Temperature/Rain Sensor | PWM | 510 | add_bytes,crc8,xor_bytes |
| Fine Offset Electronics, WH2, WH5, Telldus Temperature/Humidity/Rain Sensor | PWM | 510 | add_bytes,crc8,xor_bytes |
| Fine Offset WH1050 Weather Station | PWM | 72 | crc8 |
| HIDEKI TS04 Temperature, Humidity, Wind and Rain Sensor | DMC | — | crc8,parity8,xor_bytes |
| Holman Industries iWeather WS5029 weather station (older PWM) | FSK/PWM | 96 | lfsr_digest8_reflect,xor_bytes |
| Honeywell Door/Window Sensor, 2Gig DW10/DW11, RE208 repeater | MANCHESTER | 60 | crc16 |
| Inovalley kw9015b, TFA Dostmann 30.3161 (Rain and temperature sensor) | PPM | 36 | — |
| LaCrosse TX31U-IT, The Weather Channel WS-1910TWC-IT | FSK/PCM | — | crc8 |
| LaCrosse TX34-IT rain gauge | FSK/PCM | — | crc8 |
| LaCrosse Technology View LTV-R1, LTV-R3 Rainfall Gauge, LTV-W1/W2 Wind Sensor | FSK/PCM | 160 | crc8 |
| LaCrosse Technology View LTV-WSDTH01 Breeze Pro Wind Sensor | FSK/PCM | 264 | crc8 |
| LaCrosse WS-2310 / WS-3600 Weather Station | PWM | 52 | — |
| LaCrosse/ELV/Conrad WS7000/WS2500 weather sensors | PWM | — | add_bytes,xor_bytes |
| Missil ML0757 weather station | PPM | 40 | — |
| Oregon Scientific Weather Sensor | MANCHESTER | — | — |
| RainPoint HCS012ARF Rain Gauge sensor | PCM | 163 | add_bytes |
| RainPoint soil temperature and moisture sensor | PCM | 3000 | — |
| Sainlogic SA8, Gevanti SA8 Weather Station | PCM | — | crc16 |
| Schou 72543 Day Rain Gauge, Motonet MTX Rain, MarQuant Rain Gauge, TFA Dostmann 30.3252.01/47.3006.01 Rain Gauge and Thermometer, ADE WS1907 | PWM | — | add_bytes |
| Sharp SPC775 weather station | FSK/PWM | 48 | lfsr_digest8_reflect,xor_bytes |
| TBH weather sensor | FSK/PCM | 12 | crc16,crc8 |
| TFA 30.3151 Weather Station | FSK/PCM | 72 | crc8 |
| TFA Drop Rain Gauge 30.3233.01 | PWM | 66 | lfsr_digest8_reflect |
| Telldus weather station FT0385R sensors | MANCHESTER | 296 | crc8 |
| Thermor DG950 weather station | PWM | 9 | — |
| Vevor Wireless Weather Station 7-in-1 | FSK/PCM | 264 | add_bytes |
| WS2032 weather station | PWM | 112 | add_bytes,crc8 |

## Temperature & Humidity Sensors (72)

| Protocol | Modulation | Bits | Checksum |
|----------|------------|------|----------|
| Acurite 00275rm,00276rm Temp/Humidity with optional probe | PWM | 88 | add_bytes,crc16lsb,crc8le,lfsr_digest8,parity_bytes |
| Acurite 590TX Temperature with optional Humidity | PPM | 88 | add_bytes,crc16lsb,crc8le,lfsr_digest8,parity_bytes |
| Acurite 606TX / Technoline TX960 Temperature Sensor | PPM | 88 | add_bytes,crc16lsb,crc8le,lfsr_digest8,parity_bytes |
| Acurite 609TXC Temperature and Humidity Sensor | PPM | 88 | add_bytes,crc16lsb,crc8le,lfsr_digest8,parity_bytes |
| Acurite 986 Refrigerator / Freezer Thermometer | PPM | 88 | add_bytes,crc16lsb,crc8le,lfsr_digest8,parity_bytes |
| Acurite Grill/Meat Thermometer 01185M | PWM | 56 | add_bytes |
| Amazon Basics Meat Thermometer | PCM | 120 | — |
| Atech-WS308 temperature sensor | RZ | 58 | xor_bytes |
| Auriol AFT 77 B2 temperature sensor | PPM | 68 | add_bytes |
| Auriol AFW2A1 temperature/humidity sensor | PPM | 36 | — |
| Auriol AHFL temperature/humidity sensor | PPM | 42 | — |
| Auriol HG02832, HG05124A-DCF, Rubicson 48957 temperature/humidity sensor | PWM | 40 | crc8 |
| Baldr E0666TH Thermo-Hygrometer | PPM | 65 | — |
| Bresser Thermo-/Hygro-Sensor 3CH | PWM | 42 | — |
| Bresser Thermo-/Hygro-Sensor Explore Scientific ST1005H | PPM | 38 | — |
| Burnhard BBQ thermometer | PWM | 81 | lfsr_digest8_reflect |
| Celsia CZC1 Thermostat | PCM | 144 | crc8 |
| Companion WTR001 Temperature Sensor | PWM | 14 | parity_bytes |
| Conrad S3318P, FreeTec NC-5849-913 temperature humidity sensor, ORIA WA50 ST389 temperature sensor | PPM | 42 | crc4 |
| Danfoss CFR Thermostat | FSK/PCM | — | crc16 |
| Ecowitt Wireless Outdoor Thermometer WH53/WH0280/WH0281A | PWM | — | crc8 |
| Emos TTX201 Temperature Sensor | MANCHESTER | — | — |
| Eurochron EFTH-800 temperature and humidity sensor | PWM | 65 | crc8 |
| Eurochron temperature and humidity sensor | PPM | 36 | — |
| FT-004-B Temperature Sensor | PPM | 138 | — |
| Fine Offset Electronics WN34S/L/D and Froggit DP150/D35 temperature sensor | FSK/PCM | — | add_bytes,crc8 |
| Fine Offset Electronics, WH25, WH32, WH32B, WN32B, WH24, WH65B, HP1000, Misol WS2320 Temperature/Humidity/Pressure Sensor | FSK/PCM | 510 | add_bytes,crc8,xor_bytes |
| Fine Offset Electronics/Ecowitt WH51, WN31, SwitchDoc Labs SM23 Soil Moisture Sensor | FSK/PCM | 510 | add_bytes,crc8,xor_bytes |
| Gasmate BA1008 meat thermometer | PPM | 32 | — |
| Generic temperature sensor 1 | PPM | 24 | — |
| Homelead HG9901 (Geevon, Dr.Meter, Royal Gardineer) soil moisture/temp/light level sensor | PWM | 65 | — |
| Honeywell CM921 Wireless Programmable Room Thermostat | FSK/PCM | 60 | add_bytes |
| Hyundai WS SENZOR Remote Temperature Sensor | PPM | — | — |
| Inkbird ITH-20R temperature humidity sensor | FSK/PCM | 14563 | crc16lsb |
| Kedsum Temperature & Humidity Sensor, Pearl NC-7415 | PPM | 42 | crc4 |
| LaCrosse TX Temperature / Humidity Sensor | PWM | 44 | — |
| LaCrosse TX29IT, TFA Dostmann 30.3159.IT Temperature sensor | FSK/PCM | — | crc8 |
| LaCrosse TX35DTH-IT, TFA Dostmann 30.3155 Temperature/Humidity sensor | FSK/PCM | — | crc8 |
| LaCrosse Technology View LTV-TH Thermo/Hygro Sensor | FSK/PCM | 290 | crc8 |
| Nexus, CRX, Prego sauna temperature sensor | PPM | 37 | — |
| Nexus, FreeTec NC-7345, NX-3980, Solight TE82S, TFA 30.3209 temperature/humidity sensor | PPM | 37 | — |
| OSv1 Temperature Sensor | PWM_OSV1 | — | — |
| Opus/Imagintronix XT300 Soil Moisture | PWM | 48 | add_bytes |
| Oregon Scientific SL109H Remote Thermal Hygro Sensor | PPM | 38 | — |
| Oria WA150KM freezer and fridge thermometer | PCM | 227 | — |
| Philips outdoor temperature sensor (type AJ3650) | PWM | 112 | crc4 |
| Philips outdoor temperature sensor (type AJ7010) | PWM | 40 | xor_bytes |
| Prologue, FreeTec NC-7104, NC-7159-675 temperature sensor | PPM | 37 | — |
| Rubicson 48659 Thermometer | PPM | 33 | add_bytes |
| Rubicson Pool Thermometer 48942 | PWM | 41 | crc8 |
| Rubicson, TFA 30.3197 or InFactory PT-310 Temperature Sensor | PPM | 38 | crc8 |
| Springfield Temperature and Soil Moisture | PPM | 37 | xor_bytes |
| TFA Dostmann 14.1504.V2 Radio-controlled grill and meat thermometer | FSK/PCM | — | lfsr_digest16 |
| TFA Marbella Pool Thermometer | FSK/PCM | — | lfsr_digest8_reflect |
| TFA pool temperature sensor | PPM | 28 | — |
| TS-FT002 Wireless Ultrasonic Tank Liquid Level Meter With Temperature Sensor | PPM | 72 | xor_bytes |
| ThermoPro Meat Thermometers, TP828B 2 probes with Temp, BBQ Target LO and HI | FSK/PCM | 96 | lfsr_digest8 |
| ThermoPro Meat Thermometers, TP829B 4 probes with temp only | FSK/PCM | 96 | lfsr_digest8 |
| ThermoPro TP08/TP12/TP20 thermometer | PPM | — | lfsr_digest8_reflect |
| ThermoPro TP211B Thermometer | FSK/PCM | 64 | — |
| ThermoPro TP28b Super Long Range Wireless Meat Thermometer for Smoker BBQ Grill | FSK/PCM | 144 | add_bytes |
| ThermoPro TP862b TempSpike XR Wireless Dual-Probe Meat Thermometer | FSK/PCM | 72 | crc8 |
| ThermoPro TX-2C Thermometer and Humidity sensor | PPM | 45 | — |
| ThermoPro TX-7B Outdoor Thermometer Hygrometer | FSK/PCM | 72 | lfsr_digest8_reverse |
| ThermoPro-TX2 temperature sensor | PPM | 37 | — |
| Thermopro TP11 Thermometer | PPM | 33 | lfsr_digest8_reflect |
| WEC-2103 temperature/humidity sensor | PPM | 42 | crc4 |
| WG-PB12V1 Temperature Sensor | PWM | 48 | crc8 |
| WT0124 Pool Thermometer | PWM | 49 | add_bytes,xor_bytes |
| WallarGe CLTX001 Outdoor Temperature Sensor | PWM | — | add_bytes,parity8 |
| Watts WFHT-RF Thermostat | PWM | 54 | add_bytes |
| inFactory, nor-tec, FreeTec NC-3982-913 temperature humidity sensor | PPM | 40 | crc4 |

## TPMS (Tire Pressure) (28)

| Protocol | Modulation | Bits | Checksum |
|----------|------------|------|----------|
| AVE TPMS | FSK/PCM | 64 | crc8 |
| Abarth 124 Spider TPMS | FSK/PCM | 72 | xor_bytes |
| Airpuxem TPMS TYH11_EU6_ZQ | FSK/PCM | 84 | crc8 |
| BMW Gen2 and Gen3 TPMS | FSK/PCM | — | crc16 |
| BMW Gen4-Gen5 TPMS and Audi TPMS Pressure Alert, multi-brand HUF/Beru, Continental, Schrader/Sensata, Audi | FSK/PCM | 88 | crc8 |
| Citroen TPMS | FSK/PCM | 80 | — |
| EezTire E618, Carchet TPMS, TST-507 TPMS | MANCHESTER | — | add_bytes |
| Elantra2012 TPMS | FSK/PCM | 64 | crc8 |
| Ford TPMS | FSK/PCM | 64 | — |
| GM-Aftermarket TPMS | MANCHESTER | 130 | — |
| Hyundai TPMS (VDO) | FSK/PCM | 80 | crc8 |
| Jansite TPMS Model Solar | FSK/PCM | 88 | crc16 |
| Jansite TPMS Model TY02S | FSK/PCM | 56 | — |
| Kia TPMS (-s 1000k) | FSK/PCM | — | crc8 |
| Nissan TPMS | FSK/PCM | 37 | — |
| PMV-107J (Toyota) TPMS | FSK/PCM | — | crc8 |
| Porsche Boxster/Cayman TPMS | FSK/PCM | 80 | crc16 |
| Renault 0435R TPMS | FSK/PCM | 72 | xor_bytes |
| Renault TPMS | FSK/PCM | 72 | crc8 |
| Schrader TPMS | MANCHESTER | 120 | add_bytes,crc8,xor_bytes |
| Schrader TPMS EG53MA4, Saab, Opel, Vauxhall, Chevrolet | MANCHESTER | 120 | add_bytes,crc8,xor_bytes |
| Schrader TPMS SMD3MA4 (Subaru) 3039 (Infiniti, Nissan, Renault) | PCM | 120 | add_bytes,crc8,xor_bytes |
| Steelmate TPMS | FSK/MANCHESTER | — | add_bytes |
| TRW TPMS FSK OEM and Clone models | FSK/MANCHESTER | — | crc8 |
| TRW TPMS OOK OEM and Clone models | MANCHESTER | — | crc8 |
| Toyota TPMS | FSK/PCM | — | crc8 |
| TyreGuard 400 TPMS | MANCHESTER | 88 | crc8 |
| Unbranded SolarTPMS for trucks | FSK/PCM | 76 | xor_bytes |

## Energy & Water Meters (26)

| Protocol | Modulation | Bits | Checksum |
|----------|------------|------|----------|
| Apator Metra E-RM 30 water meter | FSK/PCM | — | crc16 |
| Arad/Master Meter Dialog3G water utility meter | FSK/MANCHESTER | 168 | — |
| Badger ORION water meter, 100kbps (-f 916.45M -s 1200k) | FSK/PCM | — | crc16 |
| BlueLine Innovations Power Cost Monitor | PPM | 32 | crc8 |
| Clipsal CMR113 Cent-a-meter power meter | PIWM_DC | 450 | — |
| ERT Interval Data Message (IDM) | MANCHESTER | 720 | crc16 |
| ERT Interval Data Message (IDM) for Net Meters | MANCHESTER | 720 | crc16 |
| ERT Standard Consumption Message (SCM) | MANCHESTER | 96 | crc16 |
| ESA1000 / ESA2000 Energy Monitor | MANCHESTER | 160 | — |
| ESIC EMT7110 power meter | FSK/PCM | 140 | add_bytes |
| Flowis flow meters | FSK/PCM | — | crc16 |
| GEO minim+ energy monitor | FSK/PCM | — | crc16 |
| IKEA Sparsnas Energy Meter Monitor | FSK/PCM | 260 | crc16 |
| Jasco/GE Choice Alert Security Devices | PCM | 87 | — |
| Landis & Gyr Gridstream Power Meters 19.2k | FSK/PCM | — | crc16 |
| Landis & Gyr Gridstream Power Meters 38.4k | FSK/PCM | — | crc16 |
| Landis & Gyr Gridstream Power Meters 9.6k | FSK/PCM | — | crc16 |
| Mueller Hot Rod water meter | FSK/PCM | 96 | crc8 |
| Neptune R900 flow meters | PCM | 168 | — |
| Orion Endpoint from Badger Meter, GIF2014W-OSE, water meter, hopping from 904.4 Mhz to 924.6Mhz (-s 1600k) | FSK/PCM | 290 | crc16 |
| Orion Endpoint from Badger Meter, GIF2020OCECNA, water meter, hopping from 904.4 Mhz to 924.6Mhz (-s 1600k) | FSK/PCM | 290 | crc16 |
| Revolt NC-5642 Energy Meter | PWM | 104 | add_bytes |
| Revolt ZX-7717 power meter | MANCHESTER | — | add_bytes |
| Standard Consumption Message Plus (SCMplus) | MANCHESTER | 128 | crc16 |
| Visonic powercode | PWM | 37 | xor_bytes |
| emonTx OpenEnergyMonitor | FSK/PCM | — | crc16lsb |

## Home Automation & Blinds (5)

| Protocol | Modulation | Bits | Checksum |
|----------|------------|------|----------|
| Markisol, E-Motion, BOFU, Rollerhouse, BF-30x, BF-415 curtain remote | PWM | 42 | — |
| RojaFlex shutter and remote devices | FSK/PCM | — | crc16 |
| Somfy RTS | PCM | 170 | xor_bytes |
| Somfy io-homecontrol | FSK/PCM | — | crc16lsb |
| Universal (Reverseable) 24V Fan Controller | PWM | 33 | xor_bytes |

## Smoke & Security Alarms (22)

| Protocol | Modulation | Bits | Checksum |
|----------|------------|------|----------|
| Bresser water leakage | FSK/PCM | 440 | crc16 |
| Cavius smoke, heat and water detector | FSK/PCM | 11 | crc8le |
| Chuango Security Technology | PWM | 25 | — |
| DSC Security Contact | RZ | 70 | crc8le |
| DSC Security Contact (WS4945) | RZ | 70 | crc8le |
| Elro DB286A Doorbell | PWM | 33 | — |
| Fine Offset / Ecowitt WH55 water leak sensor | FSK/PCM | 96 | crc8 |
| Geevon TX16-3 outdoor sensor | PWM | 73 | crc8 |
| Geevon TX19-1 outdoor sensor | PWM | 73 | lfsr_digest8_reverse |
| Generic wireless motion sensor | PWM | 20 | — |
| Govee Water Leak Detector H5054 | PWM | 48 | crc16,xor_bytes |
| Govee Water Leak Detector H5054, Door Contact Sensor B5023 | PWM | 48 | crc16,xor_bytes |
| Honeywell ActivLink, Wireless Doorbell | PWM | 48 | parity_bytes |
| Honeywell ActivLink, Wireless Doorbell (FSK) | FSK/PWM | 48 | parity_bytes |
| Interlogix GE UTC Security Devices | PPM | 64 | — |
| SimpliSafe Gen 3 Home Security System | FSK/PCM | 216 | crc16 |
| SimpliSafe Home Security System (May require disabling automatic gain for KeyPad decodes) | PIWM_DC | 92 | — |
| TFA Dostmann 30.3196 T/H outdoor sensor | FSK/MANCHESTER | 48 | lfsr_digest16 |
| TFA Dostmann 30.3221.02 T/H Outdoor Sensor (also 30.3249.02) | PWM | 41 | lfsr_digest8_reflect |
| Wireless Smoke and Heat Detector GS 558 | PWM | 27 | — |
| X10 Security | PPM | 41 | — |
| Yale HSA (Home Security Alarm), YES-Alarmkit | PWM | 13 | add_bytes |

## BBQ & Kitchen Thermometers (4)

| Protocol | Modulation | Bits | Checksum |
|----------|------------|------|----------|
| Globaltronics QUIGG GT-TMBBQ-05 | PPM | 33 | parity_bytes |
| Maverick ET-732/733 BBQ Sensor | MANCHESTER | 104 | lfsr_digest16 |
| Maverick XR-30 BBQ Sensor | FSK/PCM | 104 | lfsr_digest16 |
| Maverick XR-50 BBQ Sensor | FSK/PCM | 184 | crc8 |

## Other Sensors & Devices (77)

| Protocol | Modulation | Bits | Checksum |
|----------|------------|------|----------|
| ANT and ANT+ devices | FSK/PCM | 200 | crc16 |
| Akhan 100F14 remote keyless entry | PWM | 25 | — |
| Apator Metra E-ITN 30 heat cost allocator | FSK/PCM | — | crc16 |
| Arexx Multilogger IP-HA90, IP-TH78EXT, TSN-70E | FSK/MANCHESTER | 130 | crc8le |
| Blyss DC5-UK-WH | PWM | 33 | — |
| Brennenstuhl RCS 2044 | PWM | — | — |
| Bresser lightning | FSK/PCM | 440 | lfsr_digest16 |
| CED7000 Shot Timer | FSK/PCM | — | — |
| Calibeur RF-104 Sensor | PWM | 21 | crc8 |
| Cardin S466-TX2 | PWM | 24 | — |
| CurrentCost Current Sensor | FSK/PCM | 64 | — |
| DeltaDore X3D devices | FSK/PCM | 10 | crc16 |
| DirecTV RC66RX Remote Control | FSK/PCM | 99 | — |
| Dish remote 6.3 | PPM | 16 | — |
| ELV EM 1000 | PPM | — | — |
| ELV WS 2000 | PWM | — | — |
| EcoDHOME Smart Socket and MCEE Solar monitor | FSK/PCM | 128 | add_bytes |
| Efergy Optical | FSK/PWM | — | crc16 |
| Efergy e2 classic | FSK/PWM | — | add_bytes |
| EnOcean ERP1 | PCM | 16 | crc8 |
| Esperanza EWS | PPM | 42 | crc4 |
| FS20 / FHT | PWM | — | parity8 |
| Fine Offset Electronics WH43 air quality sensor | FSK/PCM | — | add_bytes,crc8 |
| Fine Offset Electronics WH45 air quality sensor | FSK/PCM | 240 | add_bytes,crc8 |
| Fine Offset Electronics WH46 air quality sensor | FSK/PCM | — | add_bytes,crc8 |
| Funkbus / Instafunk (Berker, Gira, Jung) | DMC | 48 | parity8,xor_bytes |
| GE Color Effects | FSK/PCM | 17 | — |
| Generic Remote SC226x EV1527 | PWM | — | — |
| Globaltronics GT-WT-02 Sensor | PPM | — | — |
| Globaltronics GT-WT-03 Sensor | PWM | — | — |
| HT680 Remote control | PWM | 41 | — |
| IBIS beacon | MANCHESTER | 250 | crc16 |
| Insteon | FSK/PCM | — | — |
| Intertechno 433 | PPM | — | — |
| Kerui PIR / Contact Sensor | PWM | 25 | — |
| KlikAanKlikUit Wireless Switch | PPM | 72 | — |
| Klimalogg | NRZS | 72 | crc8 |
| LaCrosse TX141-Bv2, TX141TH-Bv2, TX141-Bv3, TX141W, TX145wsdth, (TFA, ORIA) sensor | PWM | 64 | crc8,lfsr_digest8_reflect |
| LaCrosse Technology View LTV-WR1 Multi Sensor | FSK/PCM | 156 | crc8 |
| LightwaveRF | PPM | 91 | — |
| Marlec Solar iBoost+ sensors | FSK/PCM | 12 | crc16 |
| Maverick ET73 | PPM | 48 | — |
| Mebus 433 | PPM | — | — |
| Nexa | PPM | 72 | — |
| Norgo NGE101 | DMC | 72 | xor_bytes |
| Oil Ultrasonic SMART FSK | FSK/PCM | 64 | crc8le |
| Oil Ultrasonic STANDARD ASK | PCM | 40 | — |
| Oil Ultrasonic STANDARD FSK | FSK/PCM | 40 | — |
| Princeton PT2262/PT2264 remote | PWM | 24 | — |
| Proove / Nexa / KlikAanKlikUit Wireless Switch | PPM | 64 | — |
| Quhwa | PWM | 18 | — |
| Quinetic | FSK/PCM | 140 | crc16 |
| RF-tech | PPM | 24 | — |
| Radiohead ASK | PCM | — | crc16lsb |
| Regency Ceiling Fan Remote (-f 303.75M to 303.96M) | PWM | — | — |
| Risco 2 Way Agility protocol, Risco PIR/PET Sensor RWX95P | PCM | — | crc16 |
| Rosstech Digital Control Unit DCU-706/Sundance/Jacuzzi | PCM | 300 | xor_bytes |
| SRSmith Pool Light Remote Control SRS-2C-TX (-f 915M) | FSK/PCM | 144 | crc16,crc8 |
| Sensible Living Mini-Plant Moisture Sensor | PCM | — | crc16lsb |
| Silvercrest Remote Control | PWM | 33 | — |
| SmartFire Proflame 2 remote control | PCM | 11 | parity8 |
| Solight TE44/TE66, EMOS E0107T, NX-6876-917 | PPM | 37 | crc8 |
| TFA-Twin-Plus-30.3049, Conrad KW9010, Ea2 BL999 | PPM | 36 | — |
| Template decoder | PPM | 68 | crc8 |
| Vaillant calorMatic VRT340f Central Heating Control | DMC | 128 | add_bytes |
| Vauno EN8822C | PPM | — | — |
| WT450, WT260H, WT405H | DMC | 36 | xor_bytes |
| Watchman Sonic / Apollo Ultrasonic / Beckett Rocket oil tank monitor | FSK/PCM | 64 | crc8le |
| Watchman Sonic Advanced / Plus, Tekelek | FSK/PCM | — | crc16 |
| Waveman Switch Transmitter | PWM | — | — |
| Wireless M-Bus, Mode C&T, 100kbps (-f 868.95M -s 1200k) | FSK/PCM | — | crc16 |
| Wireless M-Bus, Mode F, 2.4kbps | FSK/PCM | — | crc16 |
| Wireless M-Bus, Mode R, 4.8kbps (-f 868.33M) | FSK/MANCHESTER | — | crc16 |
| Wireless M-Bus, Mode S, 32.768kbps (-f 868.3M -s 1000k) | FSK/PCM | — | crc16 |
| Wireless M-Bus, Mode T, 32.768kbps (-f 868.3M -s 1000k) | FSK/PCM | — | crc16 |
| X10 RF | PPM | 32 | — |
| bm5-v2 12V Battery Monitor | PWM | 88 | add_bytes |

## Protocols with Known Bitstream Layouts

These protocols have exact field positions defined, so the auto-decoder
places labels precisely on the decoded bitstream.

| Protocol | Field Layout | Bit Order |
|----------|-------------|-----------|
| HCS200/HCS300 (KeeLoq) | `encrypted(32) → id(28) → button(4) → battery(1) → repeat(1)` | LSB/BE |
| KeeLoq Generic | `encrypted(32) → id(28) → button(4)` | LSB/BE |
| FAAC SLH | `encrypted(32) → id(28) → button(4)` | LSB/BE |
| NICE Flor-S | `encrypted(32) → id(16) → button(4)` | MSB/BE |
| CAME | `id(8) → button(4)` | MSB/BE |
| Ford V0 | `id(32) → button(4) → counter(16) → checksum(12)` | MSB/BE |
| Fiat Marelli | `id(32) → button(4) → epoch(4) → counter(8) → encrypted(32)` | MSB/BE |
| KIA V6 | `id(32) → button(8) → counter(32) → encrypted(64) → checksum(8)` | MSB/BE |
| VAG VW/Audi | `id(24) → button(4) → counter(20) → encrypted(32)` | MSB/BE |
| Porsche Cayenne | `id(20) → button(4) → counter(16) → encrypted(24)` | MSB/BE |
| Somfy Telis | `checksum(4) → button(4) → counter(16) → id(24) → data(8)` | MSB/BE |
| Princeton PT2262 | `id(16) → button(4) → data(4)` | MSB/BE |

## Data Sources

- **rtl_433** (293 protocols): https://github.com/mherber/rtl_433
  - Weather stations, temperature/humidity sensors, TPMS, energy meters,
    smoke alarms, doorbells, BBQ thermometers, and many more ISM band devices
- **Flipper-ARF** (30 protocols): Flipper Zero Automotive RF firmware
  - Car key fobs (KIA, Ford, Fiat, Mazda, Mitsubishi, Subaru, Suzuki,
    Porsche, VW/Audi), gate/garage remotes (CAME, NICE, FAAC, Hormann,
    Chamberlain, Security+, Somfy), generic remotes (Princeton, Linear)

## How to Use

1. **Demodulate** your signal in URH (Interpretation tab)
2. Go to the **Analysis** tab
3. Click the **Analyze** button dropdown → **Auto-identify protocol (PHZ DB)**
4. Select a match from the ranked results
5. Click **Apply Selected Protocol**

The auto-decoder will:
- Try all available decoders (NRZ, Manchester, PWM, Miller)
- Extract the first packet if multiple repeats are present
- Strip preamble, gap/sync, and trailing padding
- Score each protocol by decoded data length match + structure
- Apply the best decoder and create field labels automatically

See [CONTRIBUTING_DECODERS.md](CONTRIBUTING_DECODERS.md) for adding new protocols.
