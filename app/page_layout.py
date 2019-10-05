# -*- coding: utf-8 -*-
import dash
import glob
import os
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dtab
import base64
#import pandas as pd
from datetime import date

this_year = date.today().strftime("%Y")
this_company = "Rippleet"
workdir = os.getcwd()
data_ext = "csv"
files = glob.glob('*.{}'.format(data_ext))
for index,value in enumerate(files):
    print index, value
#df = pd.read_csv("99co_rumah.csv")

image_filename = '/home/febrifahmi/Documents/01_CODING/Rippleet/bg_a.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Tentang kami", href="/about")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Rippleet Now",
            children=[
                dbc.DropdownMenuItem("Masuk", href="#"),
                dbc.DropdownMenuItem("Daftar", href="#"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Bantuan", href="#"),
            ],
        ),
    ],
    brand="#Rippleet",
    brand_href="/",
    sticky="top",
    style={
    	'fontColor': 'grey',
    	'fontFamily': 'Roboto',
    	}
)

body_index = dbc.Container(
    [
        # represents the URL bar for multipage support purposes, doesn't render anything
        #dcc.Location(id='url', refresh=False),
        # start the actual body here
        dbc.Row(dbc.Col(html.Div(html.Img(src='data:image/png;base64,{}'.format(encoded_image), className='container-fluid no-padding')))),
        dbc.Jumbotron(
            [
                html.H1("Rippleet", className="display-3"),
                html.P(
                    "Rippleet memiliki semangat untuk membawa data "
                    "ke hadapan pembaca dalam bentuk visualisasi data yang interaktif dan menyenangkan.",
                    className="lead",
                ),
                html.Hr(className="my-2"),
                html.P(
                    "Data kami dikumpulkan dari streaming media sosial khususnya "
                    "Twitter, dan dari berbagai laman berita online media mainstream nasional."
                ),
                html.P(html.A(dbc.Button("Pelajari lebih lanjut", color="primary", outline=True, className="lead"), href="/dashboard")),
            ]),
     	dbc.Row(dbc.Col(html.Br())),
     	dbc.Row(dbc.Col(html.Br())),
        # create footer
  #       dbc.Row(dbc.Col(html.Hr(className="my-2"))),
  #       dbc.Row(
  #   		[
		#         dbc.Col(html.Div("Hak cipta © %s %s. Seluruh hak cipta dilindungi undang-undang." %(this_year,this_company)), md=6, style={'color':"grey"}),
		#         dbc.Col(html.Div(html.A(html.Div("Kebijakan Privasi"), href="/kebijakan-privasi")), md=2, style={'color':"grey"}, className='text-center'),
  #               dbc.Col(html.Div(html.A(html.Div("Term of Use"), href="/tos")), md=2, style={'color':"grey"}, className='text-center'),
  #               dbc.Col(html.Div(html.A(html.Div("Disclaimer"), href="/disclaimer")), md=2, style={'color':"grey"}, className='text-center'),
		#     ],
		# no_gutters=True,
		# ),
		# dbc.Row(dbc.Col(html.Br())),
		# dbc.Row(
		# 	[
		# 		dbc.Col(html.Div(
		# 			[
		# 				# represents the URL bar, doesn't render anything
		# 				dcc.Location(id='url', refresh=False),

		# 				dcc.Link('Navigate to "/"', href='/'),
		# 				html.Br(),
		# 				dcc.Link('Navigate to "/page-2"', href='/page-2'),

		# 				# content will be rendered in this element
		# 				html.Div(id='page-content'),
		# 			],
		# 			)),
		# 	]),
    ],
    className="mt-4",

)

body_footer = dbc.Container(
    [
        # create footer
        dbc.Row(dbc.Col(html.Hr(className="my-2"))),
        dbc.Row(
            [
                dbc.Col(html.Div("Hak cipta © %s %s. Seluruh hak cipta dilindungi undang-undang." %(this_year,this_company)), md=6, style={'color':"grey"}),
                dbc.Col(html.Div(html.A(html.Div("Kebijakan Privasi"), href="/kebijakan-privasi")), md=2, style={'color':"grey"}, className='text-center'),
                dbc.Col(html.Div(html.A(html.Div("Term of Use"), href="/tos")), md=2, style={'color':"grey"}, className='text-center'),
                dbc.Col(html.Div(html.A(html.Div("Disclaimer"), href="/disclaimer")), md=2, style={'color':"grey"}, className='text-center'),
            ],
        no_gutters=True,
        ),
        dbc.Row(dbc.Col(html.Br())),
    ]
)

body_about = dbc.Container(
    [
        dbc.Row(dbc.Col(html.Br())),
        dbc.Row(dbc.Col(html.Div(html.H5("Tentang kami")))),
        dbc.Row(dbc.Col(html.Br())),

        html.Div(
            [
                html.P(
                    "Rippleet digagas dan mulai dibangun pada 2019, saat kontestasi politik di Indonesia sedang hangat, yang menyebabkan muncul "
                    "banyak disinformasi yang disebarkan baik melalui media sosial maupun media mainstream. Pada awalnya, kami terinspirasi dengan "
                    "beberapa platform Social Media Analytics yang telah lebih dulu ada dan berkiprah di Indonesia, yang pada saat kontestasi politik "
                    "yang hangat tersebut, banyak berperan dalam mendedah disinformasi dan mendidik netizen dengan menampilkan data."
                ),
                html.P(
                    "Namun demikian, pada perjalanannya kami melihat potensi Media Analytics Platform lebih jauh dari itu. Kami di Rippleet percaya, "
                    "bahwa media sebagai outlet ide, gagasan, kreasi, penyampaian pendapat/opini, kampanye bisnis, memiliki kekuatan positif untuk "
                    "membentuk, mendidik, dan meningkatkan literasi masyarakat terhadap data." 
                ),
                html.P(
                    "Selain itu, media memiliki nilai strategis dalam mempengaruhi pengambilan keputusan bisnis yang penting. Atas dasar inilah kami hadir "
                    "dan menawarkan akses Eksplorasi terhadap data guna perbaikan terus menerus pada bisnis Anda, di bidang apa pun anda bekerja."
                ),
                html.P(
                    "Saat ini Rippleet sedang dalam tahap pengembangan. Hubungi kami di fahmi_fafa[a.t]yahoo[d.o.t]com bila Anda tertarik untuk mendapatkan informasi lebih lanjut."
                )
            ]
        )
    ]
)

body_kebijakan_privasi = dbc.Container(
    [
        dbc.Row(dbc.Col(html.Br())),
        dbc.Row(dbc.Col(html.Div(html.H5("Kebijakan privasi")))),
        dbc.Row(dbc.Col(html.Br())),

        html.Div(
            [
                html.P("A. Informasi pribadi pengguna"),
                #html.Div(html.Br()),
                html.P(
                    "Kami berkomitmen untuk selalu menjaga privasi pengguna laman rippleet.com. "
                    "Ini berlaku untuk informasi pengguna yang disimpan di server kami.  "
                    "Data yang didapat dan dikumpulkan oleh rippleet.com yang berasal dari pihak ketiga, "
                    "seperti laman sosial media dan laman berita online, dikecualikan dari aturan ini, "
                    "dan perlindungan privasinya merupakan tanggungjawab dari laman penyedia data."
                ),
                html.Div(html.Br()),
                html.Div("B. Jenis informasi yang dikumpulkan"),
                html.Div(html.Br()),
                html.P(
                        "Jenis informasi pribadi pengguna yang kami kumpulkan baik langsung maupun melalui pihak ketiga antara lain: "
                ),
                html.Ol(
                    [
                        html.Li(html.Div("Nama pengguna")),
                        html.Li(html.Div("Username")),
                        html.Li(html.Div("Password")),
                        html.Li(html.Div("Alamat email")),
                        html.Li(html.Div("IP Address")),
                        html.Li(html.Div("Browser")),
                        html.Li(html.Div("Jaringan")),
                        html.Li(html.Div("Informasi lokasi")),
                        html.Li(html.Div("Pageview/hit")),
                        html.Li(html.Div("Sesi")),
                        html.Li(html.Div("Informasi OS")),
                        html.Li(html.Div("Tipe device")),
                        html.Li(html.Div("Referer"))
                    ]
                ),
                html.P(
                        "Sebagian besar informasi tersebut dikumpulkan dan digunakan untuk kepentingan agregasi statistik laman "
                        "dan tidak dipergunakan untuk kepentingan selain operasional akun pengguna dalam penggunaan layanan "
                        "laman rippleet.com."
                ),
                html.Div(html.Br()),
                html.Div("C. Bagaimana kami mengumpulkan informasi pengguna"),
                html.Div(html.Br()),
                html.Ol(
                    [
                        html.Li(html.Div("Offline, saat kami melakukan survey, kerjasama, maupun interview langsung dengan pengguna maupun calon pengguna layanan;")),
                        html.Li(html.Div("Melalui form isian; dan")),
                        html.Li(html.Div("Google Analytics atau layanan statistik laman sejenisnya."))
                    ]
                ),
                html.Div(html.Br()),
                html.Div("D. Informasi pribadi anak dibawah umur"),
                html.Div(html.Br()),
                html.P(
                        "Laman ini tidak mengumpulkan informasi pribadi anak-anak di bawah umur. Untuk itu, "
                        "orangtua diharapkan dapat melaporkan kepada kami bila terdapat informasi pribadi terkait "
                        "anak di bawah umur yang ditemukan di laman ini dan lolos dari pengawasan kami  mengingat data yang dikumpulkan dalam laman ini "
                        "berasal dari sosial media dan laman berita online nasional."
                        ""
                        "Penggunaan laman ini oleh anak-anak dibawah umur tidak dianjurkan."
                ),
                html.Div(html.Br()),
                html.Div("E. Perubahan"),
                html.Div(html.Br()),
                html.P(
                        "Kebijakan privasi laman ini dapat berubah sewaktu-waktu. Segala perubahan terhadap "
                        "kebijakan privasi akan ditayangkan di halaman ini."
                )
            ]
        )
    ], className="mt-12"
)

body_tos = dbc.Container(
    [
        dbc.Row(dbc.Col(html.Br())),
        dbc.Row(dbc.Col(html.Div(html.H5("Syarat dan Ketentuan")))),
        dbc.Row(dbc.Col(html.Br())),
        html.Div(
            [
                html.P(
                        "Setiap pengguna yang menggunakan laman rippleet.com menyetujui Syarat dan Ketentuan ini. "
                        "Pengguna dipersilahkan menutup laman ini apabila pengguna tidak menyetujui Syarat dan Ketentuan ini. "
                ),
                html.P(
                        "Layanan yang kami berikan kepada pengguna saat ini pada umumnya bersifat 'free of charge'. Untuk itu, kami "
                        "tidak memberikan jaminan keandalan layanan 100%. Pada saat tertentu, layanan dapat saja terganggu dikarenakan "
                        "adanya kegiatan pengembangan layanan maupun pemeliharaan rutin. "
                ),
                html.P(
                        "Pengguna layanan tidak dapat mengajukan klaim atau tuntutan kerugian akibat kehilangan data, informasi "
                        "dasbor, panel, dan akses pengguna terhadap layanan ini apabila sewaktu-waktu terdapat gangguan pada sistem."
                ),
                html.P(
                        "Pengguna dilarang melakukan aktivitas yang dapat menganggu kinerja sistem, melakukan hacking, cracking, "
                        "scraping, DoS, DDoS, dan melakukan serangan yang ditujukan ke laman rippleet.com dalam bentuk apapun. "
                        "Pelanggaran terhadap ketentuan ini dapat menimbulkan konsekuensi hukum sesuai aturan hukum Indonesia. "
                ),
                html.P(
                        "Pengguna layanan tidak diperkenankan mentransmisikan, membagikan, maupun menjual raw data yang didapatkan melalui layanan ini. "
                        "Pengguna hanya diijinkan mentransmisikan atau membagikan informasi yang merupakan hasil agregasi/analisis "
                        "data yang dilakukan, dan bukan untuk kepentingan komersial."
                )
            ]
        )

    ], className="mt-12",
)

body_disclaimer = dbc.Container(
    [
        dbc.Row(dbc.Col(html.Br())),
        dbc.Row(dbc.Col(html.Div(html.H5("Disclaimer")))),
        dbc.Row(dbc.Col(html.Br())),
        html.Div(
                html.P(
                        "Setiap penggunaan layanan, produk, data, serta informasi yang berasal dari laman ini yang tidak sesuai "
                        "dengan Syarat dan Ketentuan, bukan merupakan tanggung jawab rippleet.com dan peengelola laman ini."
                )
        ),
    ], className="mt-12",
)

body_display_details = dbc.Container(
    [
        html.Div(html.Br()),
        html.Div("Ini halaman pelajari lebih lanjut.")
    ], className="mt-12",
)

body_selected_file = dbc.Container(
    [
        html.Div(html.Br()),
        html.Div(html.H5("Explore your data:")),
        dcc.Dropdown(
            options=[
                {'label': i, 'value': i} for i in files
            ],
            placeholder="Select a file",
        ),
    ],
    className="mt-6",
)

# body_display_datatable = dbc.Container(
#     [
#         dtab.DataTable(
#             id = 'table',
#             columns = [{"name": i, "id": i} for i in df.columns],
#             data = df.to_dict('records'),
#             ),
#     ],

# )

body_grafana = dbc.Container(
    [
        dbc.Row(dbc.Col(html.Br())),
        dbc.Row(dbc.Col(html.Div(html.H5("Pelajari data Anda!")))),
        dbc.Row(dbc.Col(html.Br())),
        html.Div(
            [
                html.P(
                    "Rippleet.com memberikan akses Dasbor Grafana untuk Anda. Anda dapat "
                    "melakukan eksplorasi terhadap data yang berasal dari TwitterStreamingAPI, "
                    "dan data yang berasal dari laman berita online."
                ),
                html.P(
                    "Dengan layanan ini, Anda dapat melakukan analisis bisnis seperti: melihat "
                    "penetrasi pasar produk atau layanan anda melalui signal dari media sosial dan "
                    "laman berita online, memeriksa sentimen pelanggan terhadap suatu produk atau "
                    "layanan, mempelajari strategi business campaign kompetitor anda, dan sebagainya!"
                ),
                html.P(
                    "Akses laman Dasbor Anda di sini! Tertarik untuk mendapatkan akses ke Dasbor kami? "
                    "Kami memberikan akses gratis ke Dasbor kami dalam masa percobaan hingga akhir Juli "
                    "2019*. Manfaatkan kesempatan ini!"
                ),
                html.P(
                    "Bagi Anda yang telah memiliki akses ke Dasbor, silahkan menuju laman berikut:"
                ),
                html.P(
                    "*(Under Construction)"
                )
            ]
        ),
        html.Div(html.Br()),
        html.P(html.A(dbc.Button("Go to Dasbor!", color="primary", outline=False, className="lead"), href="http://rippleet.com:3000/"))
    ]

)




# TO DO LIST:
# body_about =
# body_rippleet =
# dsb


# Example components
# app.layout = html.Div([
#     html.Label('Dropdown'),
#     dcc.Dropdown(
#         options=[
#             {'label': 'New York City', 'value': 'NYC'},
#             {'label': u'Montréal', 'value': 'MTL'},
#             {'label': 'San Francisco', 'value': 'SF'}
#         ],
#         value='MTL'
#     ),

#     html.Label('Multi-Select Dropdown'),
#     dcc.Dropdown(
#         options=[
#             {'label': 'New York City', 'value': 'NYC'},
#             {'label': u'Montréal', 'value': 'MTL'},
#             {'label': 'San Francisco', 'value': 'SF'}
#         ],
#         value=['MTL', 'SF'],
#         multi=True
#     ),

#     html.Label('Radio Items'),
#     dcc.RadioItems(
#         options=[
#             {'label': 'New York City', 'value': 'NYC'},
#             {'label': u'Montréal', 'value': 'MTL'},
#             {'label': 'San Francisco', 'value': 'SF'}
#         ],
#         value='MTL'
#     ),

#     html.Label('Checkboxes'),
#     dcc.Checklist(
#         options=[
#             {'label': 'New York City', 'value': 'NYC'},
#             {'label': u'Montréal', 'value': 'MTL'},
#             {'label': 'San Francisco', 'value': 'SF'}
#         ],
#         values=['MTL', 'SF']
#     ),

#     html.Label('Text Input'),
#     dcc.Input(value='MTL', type='text'),

#     html.Label('Slider'),
#     dcc.Slider(
#         min=0,
#         max=9,
#         marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
#         value=5,
#     ),

#     html.Label('Button'),
#     html.Div(dcc.Input(id='input-box', type='text')),
#     html.Button('Submit', id='button'),
#     html.Div(id='output-container-button',
#              children='Enter a value and press submit'
#     ),
# ], style={'columnCount': 1})

# @app.callback(
#     dash.dependencies.Output('output-container-button', 'children'),
#     [dash.dependencies.Input('button', 'n_clicks')],
#     [dash.dependencies.State('input-box', 'value')])
# def update_output(n_clicks, value):
#     return 'The input value was "{}" and the button has been clicked {} times'.format(
#         value,
#         n_clicks
#     )