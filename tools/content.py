"""
Per-product content that only the page generator needs: long descriptions
(ID/EN) and the exact marketplace listing for each SKU.

Descriptions are written from the data in products.js (tdme.ru specs and
TDM's order form). They deliberately carry no warranty length: the carton of
SQ0335-0078 states 1 year while the site says 3 years for the range, and
that claim is still to be confirmed per product.

TOKOPEDIA paths are relative to https://www.tokopedia.com/tdm-electric/ and
were read from the live store on 2026-09-25. Where a listing has colour or
switch variants, the path ends in the variant's SKU id so the right variant
opens. SQ0504-0003 is on Tokopedia but its product page could not be read,
so it falls back to the store page. Products without a Tokopedia listing are
omitted and get no Tokopedia button.

BLIBLI is the store's product code; https://www.blibli.com/product-detail-
<code with dots>.html redirects to the live listing.
"""

TOKOPEDIA_STORE = "https://www.tokopedia.com/tdm-electric"

TOKOPEDIA = {
    "SQ1806-0405": "grounded-angled-plug-steker-arde-bengkok-1737493947474347147-1737494285086852235",
    "SQ1806-0406": "grounded-angled-plug-steker-arde-bengkok-1737493947474347147-1737494303664931979",
    "SQ1806-0411": "stop-kontak-kabel-female-16a-250v-dengan-grounding-1737515211012277387-1737515385447220363",
    "SQ1806-0412": "stop-kontak-kabel-female-16a-250v-dengan-grounding-1737515211012277387-1737515385447285899",
    "SQ1806-0003": "steker-listrik-straight-16a-250v-dengan-grounding-1737514515499680907-1737514597809226891",
    "SQ1806-0004": "steker-listrik-straight-16a-250v-dengan-grounding-1737514515499680907-1737514597809292427",
    "SQ1806-0009": "steker-siku-dengan-saklar-grounding-16a-250v-plug-listrik-tdm-1737514436357227659",
    "SQ1818-0001": "saklar-listrik-tahan-air-indoor-outdoor-1737493753644221579-1737493832806728843",
    "SQ1818-0002": "saklar-listrik-tahan-air-indoor-outdoor-1737493753644221579-1737493832806794379",
    "SQ1818-0009": "stop-kontak-outdoor-tahan-air-dengan-cover-1737493807277573259",
    "SQ1804-0011": "stop-kontak-dengan-penutup-grounding-16a-250v-ip44-1737515131091584139",
    "SQ1824-0010": "stop-kontak-2-lubang-surface-mount-16a-250v-grounding-1737514613938095243",
    "SQ0502-0001": "skun-ring-nki-1-25-4-konektor-kabel-merah-100-pcs-untuk-listrik-1737333201469998219",
    "SQ0504-0003": None,  # listed, product page not readable: store page
    "SQ0512-0006": "skun-ferrule-e10-12-10mm-isi-100-pcs-skun-pin-kabel-berisolasi-tdm-1737348585127642251",
    "SQ0335-0047": "pendant-lamp-holder-fitting-dudukan-lampu-gantung-1737332533249016971-1737332676107535499",
    "SQ0335-0050": "pendant-lamp-holder-fitting-dudukan-lampu-gantung-1737332533249016971-1737332676107601035",
    "SQ0335-0078": "wall-lampholder-heat-resistant-soket-lampu-tahan-panas-1737332963013526667",
    "SQ1809-0023": "konektor-antena-f-female-to-f-female-f-socket-coupler-tdm-sq1809-0023-1737348849143547019",
    "SQ1010-0101": "tdm-electric-insulated-side-cutters-160mm-alat-pemotong-sisi-terisolasi-dengan-panjang-160mm-1737332273340449931",
    "SQ1010-0103": "insulated-long-nose-pliers-160mm-tang-lancip-berisolasi-1737332387527492747",
    "SQ1017-0101": "insulated-tool-set-8pcs-set-peralatan-teknisi-listrik-berisolasi-profesional-1737331985918166155",
}

BLIBLI = {
    "SQ1806-0405": "TDE-70004-00001", "SQ1818-0009": "TDE-70004-00002", "SQ1815-0025": "TDE-70004-00003",
    "SQ1804-0011": "TDE-70004-00004", "SQ1805-0019": "TDE-70004-00005", "SQ1824-0010": "TDE-70004-00006",
    "SQ0502-0001": "TDE-70004-00007", "SQ0504-0003": "TDE-70004-00008", "SQ0512-0006": "TDE-70004-00009",
    "SQ0512-0022": "TDE-70004-00010", "SQ0541-0004": "TDE-70004-00011", "SQ1806-0406": "TDE-70004-00012",
    "SQ0335-0047": "TDE-70004-00013", "SQ0335-0050": "TDE-70004-00014", "SQ1010-0101": "TDE-70004-00015",
    "SQ1010-0103": "TDE-70004-00016", "SQ1017-0101": "TDE-70004-00017", "SQ1806-0411": "TDE-70004-00018",
    "SQ1806-0412": "TDE-70004-00019", "SQ1806-0003": "TDE-70004-00020", "SQ1806-0004": "TDE-70004-00021",
    "SQ1806-0009": "TDE-70004-00022", "SQ1818-0001": "TDE-70004-00023", "SQ1818-0002": "TDE-70004-00024",
    "SQ1809-0021": "TDE-70004-00025", "SQ1809-0022": "TDE-70004-00026", "SQ1809-0023": "TDE-70004-00027",
    "SQ0335-0078": "TDE-70004-00028",
}


def tokopedia_url(sku):
    if sku not in TOKOPEDIA:
        return None
    path = TOKOPEDIA[sku]
    return f"{TOKOPEDIA_STORE}/{path}" if path else TOKOPEDIA_STORE


def blibli_url(sku):
    code = BLIBLI.get(sku)
    return f"https://www.blibli.com/product-detail-{code.replace('-', '.')}.html" if code else None


# (Indonesian, English)
DESC = {
    "SQ1806-0405": (
        "Steker sudut 90 derajat dengan kontak arde, cocok untuk colokan di balik perabot karena tidak menonjol jauh dari dinding. Bodi termoplastik ABS dengan penahan kabel, rating 16A 250V. Dilengkapi lubang gantung pada bodi untuk memudahkan penyimpanan.",
        "A 90-degree angled plug with earth contact, made for sockets behind furniture because it sits close to the wall. ABS thermoplastic body with a cable clamp, rated 16A 250V. A hanging eyelet on the body makes it easy to store."),
    "SQ1806-0406": (
        "Steker sudut 90 derajat dengan kontak arde dalam warna hitam, cocok untuk colokan di balik perabot karena tidak menonjol jauh dari dinding. Bodi termoplastik ABS dengan penahan kabel, rating 16A 250V. Dilengkapi lubang gantung pada bodi.",
        "A black 90-degree angled plug with earth contact, made for sockets behind furniture because it sits close to the wall. ABS thermoplastic body with a cable clamp, rated 16A 250V, with a hanging eyelet on the body."),
    "SQ1806-0411": (
        "Stop kontak kabel (betina) 2P+arde untuk menyambung atau memperpanjang kabel listrik. Kontak kuningan berlapis nikel agar sambungan tetap stabil, bodi ABS dengan penjepit kabel di dalam. Rating 16A 250V.",
        "An in-line 2P+E socket (female) for joining or extending a power cable. Nickel-plated brass contacts keep the connection stable, and the ABS body has an internal cable clamp. Rated 16A 250V."),
    "SQ1806-0412": (
        "Stop kontak kabel (betina) 2P+arde warna hitam untuk menyambung atau memperpanjang kabel listrik. Bodi termoplastik dengan penjepit kabel di dalam, rating 16A 250V.",
        "A black in-line 2P+E socket (female) for joining or extending a power cable. Thermoplastic body with an internal cable clamp, rated 16A 250V."),
    "SQ1806-0003": (
        "Steker lurus dengan kontak arde, sanggup menangani beban hingga 4000W pada 16A 250V. Bodi ABS tahan benturan dengan pegangan bergerigi sehingga mudah dicabut tanpa menarik kabel.",
        "A straight plug with earth contact that handles loads up to 4000W at 16A 250V. Impact-resistant ABS body with a ribbed grip, so it can be unplugged without pulling on the cable."),
    "SQ1806-0004": (
        "Steker lurus warna hitam dengan kontak arde dan bodi plastik tahan benturan, rating 16A 250V. Bentuk memanjang dengan permukaan bergerigi memudahkan pencabutan tanpa menarik kabel.",
        "A black straight plug with earth contact and an impact-resistant plastic body, rated 16A 250V. Its long ribbed body makes it easy to unplug without pulling on the cable."),
    "SQ1806-0009": (
        "Steker sudut dengan saklar on/off terpasang di bodi, sehingga alat dapat dimatikan tanpa mencabut colokan. Bodi ABS self-extinguishing (tidak merambatkan api), rating 16A 250V.",
        "An angled plug with an on/off switch built into the body, so an appliance can be switched off without unplugging it. Self-extinguishing ABS body, rated 16A 250V."),
    "SQ1818-0001": (
        "Saklar tunggal pasang tempel untuk area lembap seperti teras, kamar mandi, garasi, dan gudang. Tingkat proteksi IP44 menahan cipratan air dari segala arah, rating 10A 250V.",
        "A single surface-mounted switch for damp areas such as terraces, bathrooms, garages and storerooms. IP44 protection keeps out splashing water from any direction; rated 10A 250V."),
    "SQ1818-0002": (
        "Saklar ganda 2 gang pasang tempel untuk mengatur dua titik lampu dari satu posisi. Tingkat proteksi IP44 menahan cipratan air, cocok untuk teras, garasi, dan area semi-outdoor. Rating 10A 250V.",
        "A two-gang surface-mounted switch that controls two lights from one position. IP44 protection keeps out splashing water, suited to terraces, garages and semi-outdoor areas. Rated 10A 250V."),
    "SQ1818-0009": (
        "Stop kontak ganda pasang tempel dengan tutup transparan berengsel. Proteksi IP54 menahan debu dan cipratan air sehingga aman untuk teras, taman, dan garasi. Rating 16A 250V dengan kontak arde.",
        "A double surface-mounted socket with a hinged transparent cover. IP54 protection keeps out dust and splashing water, making it safe for terraces, gardens and garages. Rated 16A 250V with earth contact."),
    "SQ1815-0025": (
        "Stop kontak ganda tanam (inbow) dua lubang dengan kontak arde dalam satu frame. Faceplate polikarbonat yang rata memudahkan pembersihan, rating 16A 250V. Dipasang pada kotak tanam standar dengan cakar dan sekrup.",
        "A double flush-mounted socket with two earthed outlets in one frame. The flat polycarbonate faceplate is easy to clean; rated 16A 250V. Fits a standard flush box with claws and screws."),
    "SQ1804-0011": (
        "Stop kontak dengan tutup flip berpegas yang menutup sendiri saat colokan dicabut, menahan debu dan cipratan air pada tingkat IP44. Bodi ABS bebas halogen dengan kontak fosfor-perunggu, rating 16A.",
        "A socket with a spring-loaded flip cover that closes by itself when unplugged, keeping out dust and splashes to IP44. Halogen-free ABS body with phosphor-bronze contacts, rated 16A."),
    "SQ1805-0019": (
        "Stop kontak seri Onega dengan tutup flip berpegas yang menutup sendiri, proteksi IP44 terhadap debu dan cipratan air. Bahan plastik bebas halogen sehingga lebih aman bila terkena panas. Rating 16A 250V.",
        "An Onega-series socket with a self-closing spring flip cover and IP44 protection against dust and splashes. Halogen-free plastic behaves more safely under heat. Rated 16A 250V."),
    "SQ1824-0010": (
        "Stop kontak ganda pasang tempel (outbow) dengan kontak arde, praktis untuk menambah titik colokan tanpa membongkar dinding. Bodi termoplastik, rating 16A 250V.",
        "A double surface-mounted socket with earth contact, a simple way to add outlets without opening the wall. Thermoplastic body, rated 16A 250V."),
    "SQ0502-0001": (
        "Skun ring (sepatu kabel) NKI 1.25-4 untuk ujung kabel serabut 0,5-1,5 mm2 pada terminal berbaut. Konduktor kuningan dengan isolasi PVC di pangkalnya agar sambungan rapi dan tidak mudah lepas. Dikemas isi 100 pcs.",
        "NKI 1.25-4 insulated ring terminals for 0.5-1.5 mm2 stranded wire on bolted terminals. Brass conductor with a PVC-insulated barrel for a neat connection that stays put. Pack of 100."),
    "SQ0504-0003": (
        "Konektor female pipih RpIm 1.25-250 untuk sambungan cepat tanpa baut pada kabel hingga 1,5 mm2. Konduktor kuningan berlapis nikel dengan isolasi PVC, sering dipakai pada panel, otomotif, dan perbaikan alat listrik. Dikemas isi 100 pcs.",
        "RpIm 1.25-250 insulated flat female connectors for quick, boltless joins on wire up to 1.5 mm2. Nickel-plated brass with PVC insulation, common in panels, automotive work and appliance repair. Pack of 100."),
    "SQ0512-0006": (
        "Ferrule berisolasi E10-12 untuk merapikan ujung kabel serabut 10 mm2 sebelum masuk terminal. Panjang pin 12 mm, konduktor kuningan dengan kepala isolasi polipropilen. Dipasang dengan tang crimping. Dikemas isi 100 pcs.",
        "E10-12 insulated ferrules that finish 10 mm2 stranded wire before it goes into a terminal. 12 mm pin, brass conductor, polypropylene collar. Fitted with a crimping tool. Pack of 100."),
    "SQ0512-0022": (
        "Ferrule berisolasi E4012 untuk kabel serabut 4 mm2 dengan panjang pin 12 mm. Konduktor kuningan berlapis timah dengan kepala isolasi polipropilen, menjaga serabut tetap menyatu di dalam terminal. Dikemas isi 100 pcs.",
        "E4012 insulated ferrules for 4 mm2 stranded wire, 12 mm pin. Tin-plated brass with a polypropylene collar keeps every strand together inside the terminal. Pack of 100."),
    "SQ0541-0004": (
        "Capit buaya berisolasi ZKI 5A dengan panjang klip 46 mm, untuk pengukuran dan sambungan sementara saat pengujian rangkaian. Selongsong PVC menutup bagian logam sehingga mengurangi risiko korsleting antar klip. Dikemas isi 10 pcs.",
        "ZKI 5A insulated alligator clips, 46 mm long, for measurements and temporary connections while testing circuits. A PVC sleeve covers the metal to reduce the risk of shorts between clips. Pack of 10."),
    "SQ0335-0047": (
        "Fitting lampu gantung E27 gaya Loft warna hitam dari keramik dan metal, tahan panas lebih baik daripada fitting plastik. Cocok untuk bohlam dekoratif pada kafe, ruang tamu, maupun area industrial. Sudah dilengkapi braket dan kabel.",
        "A black Loft-style E27 pendant lampholder in ceramic and metal, which handles heat better than plastic holders. Suited to decorative bulbs in cafes, living rooms and industrial interiors. Comes with bracket and cable."),
    "SQ0335-0050": (
        "Fitting lampu gantung E27 gaya Loft dengan finishing tembaga dari keramik dan metal, tahan panas lebih baik daripada fitting plastik. Cocok untuk bohlam dekoratif bergaya industrial pada 220V.",
        "A copper-finish Loft-style E27 pendant lampholder in ceramic and metal, which handles heat better than plastic holders. Made for decorative industrial-style bulbs on 220V."),
    "SQ0335-0078": (
        "Fitting lampu dinding E27 model miring dari plastik tahan panas, cocok untuk bohlam di teras, gudang, kamar mandi, maupun area servis. Bodi hitam dipasang langsung ke dinding atau plafon dengan sekrup.",
        "An angled E27 wall lampholder in heat-resistant plastic, for bulbs on terraces, in storerooms, bathrooms and service areas. The black body screws straight onto a wall or ceiling."),
    "SQ1809-0021": (
        "Konektor F-type berulir untuk kabel coaxial RG6 dengan impedansi 75 Ohm. Badan logam berlapis nikel sehingga tahan korosi dan kontaknya stabil. Pemasangan tanpa solder, cukup dipilin pada ujung kabel. Dikemas isi 100 pcs, praktis untuk instalasi antena, CCTV, parabola, maupun stok toko.",
        "A threaded F-type connector for 75 Ohm RG6 coaxial cable. Nickel-plated metal body resists corrosion and keeps contact stable. No soldering: it twists onto the cable end. Pack of 100, for antenna, CCTV and satellite installs or shop stock."),
    "SQ1809-0022": (
        "Adaptor konektor F ke steker TV 75 Ohm untuk menyambungkan kabel coaxial berkonektor F ke port antena televisi. Badan logam berlapis nikel sehingga tahan korosi dan sinyal tetap stabil. Dikemas isi 100 pcs, praktis untuk instalasi maupun stok toko.",
        "A 75 Ohm F-socket to TV-plug adapter that connects F-terminated coaxial cable to a television's aerial port. Nickel-plated metal body resists corrosion and keeps the signal stable. Pack of 100, for installers or shop stock."),
    "SQ1809-0023": (
        "Adaptor konektor F female ke F female 75 Ohm untuk menyambung dua kabel coaxial berkonektor F menjadi satu jalur lebih panjang. Badan logam berlapis nikel, tahan korosi dan menjaga kualitas sinyal. Dikemas isi 100 pcs.",
        "A 75 Ohm F-female to F-female coupler that joins two F-terminated coaxial cables into one longer run. Nickel-plated metal body resists corrosion and preserves signal quality. Pack of 100."),
    "SQ1010-0101": (
        "Tang potong dielektrik 160 mm bersertifikat VDE 1000V untuk pekerjaan pada instalasi bertegangan. Rahang baja CR-V dengan gagang dielektrik berlapis TPR yang tidak licin di tangan.",
        "160 mm dielectric side cutters, VDE-rated to 1000V for work on live installations. CR-V steel jaws with TPR-coated dielectric handles that don't slip in the hand."),
    "SQ1010-0103": (
        "Tang lancip dielektrik 160 mm bersertifikat VDE 1000V untuk menjangkau dan membentuk kabel di ruang sempit. Rahang baja CR-V dengan gagang dielektrik berlapis TPR yang nyaman digenggam.",
        "160 mm dielectric long-nose pliers, VDE-rated to 1000V, for reaching and shaping wire in tight spaces. CR-V steel jaws with comfortable TPR-coated dielectric handles."),
    "SQ1017-0101": (
        "Set perkakas dielektrik 1000V isi 8 pcs berisi tang dan obeng berisolasi untuk teknisi listrik. Seluruh bagian logam terbuat dari baja CR-V dan gagangnya berisolasi untuk pekerjaan pada instalasi bertegangan. Dikemas dalam tas kain agar mudah dibawa.",
        "An 8-piece 1000V dielectric tool set of insulated pliers and screwdrivers for electricians. All metal parts are CR-V steel with insulated handles for work on live installations. Packed in a cloth bag for carrying."),
}

# Warranty differs from the site-wide default only where the carton says so.
WARRANTY_YEARS = {"SQ0335-0078": 1}
