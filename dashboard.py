# Libraries in use
# Database
import pymongo
# Dashboard
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
# Timescale for graphs
from datetime import datetime, timedelta

# Dashboard initialisation
app = dash.Dash(__name__)
app.css.config.serve_locally = False
app.title = 'Virtual Manager'
app.css.append_css({'external_url':'https://codepen.io/chriddyp/pen/bWLwgP.css'})

# Navigation bar
app.layout = html.Div([
    html.Div([
        html.H1('Virtual Monitor',style={
            'padding': '10px',
            'margin':'0',
            'border': '0',
            'color': '#FFFFFF',
            'backgroundColor':'#263240'}),
        html.Div([
            dcc.Tabs(id="tabs", value='tabs', children=[
                dcc.Tab(label='System', value='system'),
                dcc.Tab(label='Virtual Machines', value='virtual-machine'),
                dcc.Tab(label='Deploy', value='Deploy'),
            ]),
            html.Div(id='tabs-content'),
        ],className='row')
    ]),

    # Server settings menu
    html.Div([

    ], className="four columns", style={'backgroundColor': '#263240', 'padding': '10px'}),
    html.Div([
        html.Div([
            html.Form([
                html.H3('Server settings', style={'color': '#0000000', 'text-align': 'center'}),
                html.Div([
                    html.H6('Server address', style={'color': '#0000000'}),
                    dcc.Input(value='', type='text', className="eleven columns"),
                ], className="row"),
                html.Div([
                    html.H6('Username', style={'color': '#0000000'}),
                    dcc.Input(value='', type='text', className="eleven columns",
                              style={}),
                ], className="row"),
                html.Div([
                    html.H6('Password', style={'color': '#0000000'}),
                    dcc.Input(value='', type='password', className="eleven columns",
                              style={"padding": "20px"}),
                ], className="row"),
                html.Div([
                    html.Button('Submit', id='button',
                                style={'color': '#FFFFFF', 'backgroundColor': '#111111'}, className="twelve columns")
                ], className='row', style={'padding':'20px'})

            ])
        ], className="four columns", style={'backgroundColor': '#e8f4f7', 'padding': '10px', 'padding-bottom':'10px','text-align': 'center'})
    ], className='row'),
    html.Div([

    ],className="row", style={'backgroundColor':'#263240'})
],className="row", style={'backgroundColor':'#263240'})

# Interactive pages
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    # List of date times for graphs
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    minus5 = timedelta(minutes=-5)
    now_minus_5 = datetime.now() + minus5
    current_time_minus_5 = now_minus_5.strftime("%H:%M")
    now_minus_10 = datetime.now() + minus5*2
    current_time_minus_10 = now_minus_10.strftime("%H:%M")
    now_minus_15 = datetime.now() + minus5*3
    current_time_minus_15 = now_minus_15.strftime("%H:%M")
    now_minus_20 = datetime.now() + minus5*4
    current_time_minus_20 = now_minus_20.strftime("%H:%M")
    now_minus_25 = datetime.now() + minus5*5
    current_time_minus_25 = now_minus_25.strftime("%H:%M")
    now_minus_30 = datetime.now() + minus5*6
    current_time_minus_30 = now_minus_30.strftime("%H:%M")

    # System information dashboard
    if tab == 'system':
        return html.Div([
            html.Div([
                html.H3(children='Resources', style={
                    'textAlign': 'center',
                    'color': '#ffffff',
                    'backgroundColor':'#52687a',
                    'padding': '10px'}),

                # Graphs of CPU, RAM and Storage
                html.Div([
                    html.Div([

                        dcc.Graph(id='live-update-graph',
                                  figure=dict(
                                      data=[
                                          dict(
                                              x=[current_time_minus_30, current_time_minus_25, current_time_minus_20,
                                                 current_time_minus_15, current_time_minus_10, current_time_minus_5,
                                                 current_time],
                                              y=[ 90, 92, 93, 93, 92, 91, 94],
                                              name="CPU",
                                              marker=dict(
                                                  color='rgb(55, 83, 109)'
                                              )
                                          )
                                      ],
                                      layout=dict(
                                          plot_bgcolor='#E8F4F7',
                                          paper_bgcolor='#E8F4F7',
                                          textfont= dict(color='#ffffff'),
                                          title='CPU usage %',
                                          height=400,
                                          showlegend=True,

                                          legend=dict(
                                              x=0,
                                              y=1.0
                                          ),
                                          margin=dict(l=40, r=0, t=40, b=30)
                                      ),
                                  ),
                                  )

                    ],className="four columns", style={'backgroundColor':'#263240', 'padding': '10px'}),

                    html.Div([
                        dcc.Graph(
                            figure=dict(
                                data=[
                                    dict(
                                        x=[current_time_minus_30, current_time_minus_25, current_time_minus_20,
                                           current_time_minus_15, current_time_minus_10, current_time_minus_5,
                                           current_time],
                                        y=[64, 64, 64, 65,
                                           62, 60],
                                        name='RAM',
                                        marker=dict(
                                            color='rgb(26, 118, 255)'
                                        )
                                    )

                                ],
                                layout=dict(
                                    title='RAM usage %',
                                    showlegend=True,
                                    plot_bgcolor='#E8F4F7',
                                    paper_bgcolor='#E8F4F7',
                                    height = 400,
                                    legend=dict(
                                        x=0,
                                        y=1.0
                                    ),
                                    margin=dict(l=40, r=0, t=40, b=30)
                                ),
                            ),
                        )

                    ], className="four columns", style={'backgroundColor':'#263240', 'padding': '10px'}),
                    html.Div([
                        dcc.Graph(
                            figure=dict(
                                data=[
                                    dict(
                                        x=[current_time_minus_30, current_time_minus_25, current_time_minus_20,
                                           current_time_minus_15, current_time_minus_10, current_time_minus_5,
                                           current_time],
                                        y=[56, 56, 56, 56,
                                           56, 56,],
                                        name='Storage',
                                        marker=dict(
                                            color='rgb(2, 168, 25)'
                                        )
                                    )
                                ],
                                layout=dict(
                                    title='Disk usage %',
                                    height=400,
                                    showlegend=True,
                                    plot_bgcolor='#E8F4F7',
                                    paper_bgcolor='#E8F4F7',
                                    legend=dict(
                                        x=0,
                                        y=1.0
                                    ),
                                    margin=dict(l=40, r=0, t=40, b=30)
                                ),
                            ),
                        )

                    ], className="four columns", style={'backgroundColor':'#263240', 'padding': '10px'})
                ]),


            ], className="row", style={'backgroundColor':'#263240', 'bottom': '100px'}),
            # Detailed information on system
            html.Div([
                html.H6('CPU Cores: '+ str(cpu_cores())),
                html.H6('CPU Threads: '+ str(cpu_threads())),
                html.H6('CPU Sockets: '+ str(cpu_sockets())),
                html.H6('CPU Model: '+ str(cpu_model())),
                html.H6('Memory: '+ str(memory_size())+ " GB"),
                html.H6('Total Storage: ' + str(total_storage()) + " GB"),
                html.H6('Vendor: '+ str(vendor())),
                html.H6('Model: '+ str(model())),
                html.H6('Server IP: '+ str(server_IP())),
                html.H6('vCenter IP: '+ str(vcenter_IP())),
                html.H6('No. Network Interfaces: '+ str(network_interfaces()))

            ], style={'backgroundColor': '#e8f4f7'}),
        ])

# Virtual machine informaion dashboard
    elif tab == 'virtual-machine':

        return html.Div([
            html.Div([
                html.Div([
                    html.H3(children='Virtual Machines', style={
                        'textAlign': 'center',
                        'color': '#ffffff',
                        'backgroundColor': '#3d4e5c',
                        'padding': '20px'}),
                ], className= 'row', style={'backgroundColor': '#111111'}),

                # Virtual machine information boxes
                html.Div([
                    html.Div([
                        html.H6("Name:  " + str(virtualMachines('name', 0)), style={'color': '#FFFFFF'}),
                        html.H6("Machine Type:  " + str(virtualMachines('guest', 0)), style={'color': '#FFFFFF'}),
                        html.H6("Description:  " + str(virtualMachines('description', 0)), style={'color': '#FFFFFF'}),
                        html.H6("Power State:  " + str(virtualMachines('power_state', 0)), style={'color': '#FFFFFF'}),
                        html.H6("IP Address:  " + str(virtualMachines('ipaddress', 0)), style={'color': '#FFFFFF'}),
                        html.H6("Memory  " + str(round(virtualMachines('host_memory', 0)/1024, 1)) + "GB", style={'color': '#FFFFFF'}),
                        html.H6("Assigned Disk:  " + str(round(virtualMachines('host_storage_assigned', 0)/(2**30), 2)) + "GB", style={'color': '#FFFFFF'}),
                        html.H6("Disc Usage:  " + str(round(virtualMachines('vm_storage_usage', 0)/(2**30), 2)) + "GB", style={'color': '#FFFFFF'})
                    ], className="six columns", style={'backgroundColor': '#3d4e5c', 'padding': '10px'}),

                    html.Div([
                        html.H6("Name:  " + str(virtualMachines('name', 1)), style={'color': '#FFFFFF'}),
                        html.H6("Machine Type:  " + str(virtualMachines('guest', 1)), style={'color': '#FFFFFF'}),
                        html.H6("Description:  " + str(virtualMachines('description', 1)), style={'color': '#FFFFFF'}),
                        html.H6("Power State:  " + str(virtualMachines('power_state', 1)), style={'color': '#FFFFFF'}),
                        html.H6("IP Address:  " + str(virtualMachines('ipaddress', 1)), style={'color': '#FFFFFF'}),
                        html.H6("Memory  " + str(round(virtualMachines('host_memory', 1) / 1024, 1)) + "GB", style={'color': '#FFFFFF'}),
                        html.H6("Assigned Disk:  " + str(round(virtualMachines('host_storage_assigned', 1) / (2 ** 30), 2)) + "GB", style={'color': '#FFFFFF'}),
                        html.H6("Disc Usage:  " + str(round(virtualMachines('vm_storage_usage' , 1) / (2 ** 30), 2)) + "GB", style={'color': '#FFFFFF'})
                    ], className="six columns", style={'backgroundColor': '#3d4e5c', 'padding': '10px'}),
                ], className= 'row',style={'backgroundColor': '#111111'}),

                html.Div([
                    html.Div([
                        html.H6("Name:  " + str(virtualMachines('name', 2)), style={'color': '#FFFFFF'}),
                        html.H6("Machine Type:  " + str(virtualMachines('guest', 2)), style={'color': '#FFFFFF'}),
                        html.H6("Description:  " + str(virtualMachines('description', 2)), style={'color': '#FFFFFF'}),
                        html.H6("Power State:  " + str(virtualMachines('power_state', 2)), style={'color': '#FFFFFF'}),
                        html.H6("IP Address:  " + str(virtualMachines('ipaddress', 2)), style={'color': '#FFFFFF'}),
                        html.H6("Memory  " + str(round(virtualMachines('host_memory', 2) / 1024, 1)) + "GB",
                                style={'color': '#FFFFFF'}),
                        html.H6("Assigned Disk:  " + str(
                            round(virtualMachines('host_storage_assigned', 2) / (2 ** 30), 2)) + "GB",
                                style={'color': '#FFFFFF'}),
                        html.H6(
                            "Disc Usage:  " + str(round(virtualMachines('vm_storage_usage', 2) / (2 ** 30), 2)) + "GB",
                            style={'color': '#FFFFFF'})
                    ], className="six columns", style={'backgroundColor': '#3d4e5c', 'padding': '10px'}),

                    html.Div([
                        html.H6("Name:  " + str(virtualMachines('name', 3)), style={'color': '#FFFFFF'}),
                        html.H6("Machine Type:  " + str(virtualMachines('guest', 3)), style={'color': '#FFFFFF'}),
                        html.H6("Description:  " + str(virtualMachines('description', 3)), style={'color': '#FFFFFF'}),
                        html.H6("Power State:  " + str(virtualMachines('power_state', 3)), style={'color': '#FFFFFF'}),
                        html.H6("IP Address:  " + str(virtualMachines('ipaddress', 3)), style={'color': '#FFFFFF'}),
                        html.H6("Memory  " + str(round(virtualMachines('host_memory', 3) / 1024, 1)) + "GB", style={'color': '#FFFFFF'}),
                        html.H6("Assigned Disk:  " + str(round(virtualMachines('host_storage_assigned', 3) / (2 ** 30), 2)) + "GB", style={'color': '#FFFFFF'}),
                        html.H6("Disc Usage:  " + str(round(virtualMachines('vm_storage_usage', 3) / (2 ** 30), 2)) + "GB", style={'color': '#FFFFFF'})
                    ], className="six columns", style={'backgroundColor': '#3d4e5c', 'padding': '10px'}),
                ], className='row', style={'backgroundColor': '#111111', 'padding': '10px'}),

                html.Div([
                    html.Div([
                        html.H6("Name:  " + str(virtualMachines('name', 4)), style={'color': '#FFFFFF'}),
                        html.H6("Machine Type:  " + str(virtualMachines('guest', 4)), style={'color': '#FFFFFF'}),
                        html.H6("Description:  " + str(virtualMachines('description', 4)), style={'color': '#FFFFFF'}),
                        html.H6("Power State:  " + str(virtualMachines('power_state', 4)), style={'color': '#FFFFFF'}),
                        html.H6("IP Address:  " + str(virtualMachines('ipaddress', 4)), style={'color': '#FFFFFF'}),
                        html.H6("Memory  " + str(round(virtualMachines('host_memory', 4) / 1024, 1)) + "GB", style={'color': '#FFFFFF'}),
                        html.H6("Assigned Disk:  " + str(round(virtualMachines('host_storage_assigned', 4) / (2 ** 30), 2)) + "GB", style={'color': '#FFFFFF'}),
                        html.H6("Disc Usage:  " + str(round(virtualMachines('vm_storage_usage', 4) / (2 ** 30), 2)) + "GB", style={'color': '#FFFFFF'})
                    ], className="six columns", style={'backgroundColor': '#3d4e5c', 'padding': '10px'}),
                ], className='row', style={'backgroundColor': '#111111', 'padding': '10px'}),
            ], className="twelve columns", style={'backgroundColor': '#111111',}),
        ],style={'backgroundColor': '#263240'}),
        html.Div([
            html.h3('vm', style={'color': '#FFFFFF', 'text-align': 'center'}),
        ],style={'backgroundColor': '#263240', 'padding': '50px'})

    # Virtual machine deployment page
    elif tab == 'Deploy':
        return html.Div([
            html.Div([
                # Deployment form
                html.Form([
                    html.H3('Deploy VM', style={'color': '#FFFFFF', 'text-align': 'center'}),
                    html.Div([
                        html.H6('VM Name', style={'color': '#FFFFFF'}),
                        dcc.Input(value='', type='text', className="ten columns"),
                    ], className="row"),
                    html.Div([
                        html.H6('Description', style={'color': '#FFFFFF'}),
                        dcc.Input(value='', type='text', className="ten columns", style={'backgroundColor': '#3d4e5c', "padding": "20px"}),
                    ], className="row"),
                    html.H6('RAM', style={'color': '#FFFFFF'}),
                    # Auto adjusting slider
                    dcc.Slider(
                        min=0,
                        max=round(avaliable_resources('memory')),
                        marks={i: '1'.format(i) if i == 1 else str(i) for i in range(1, 32)},
                        value=1,
                    ),
                    html.H6('CPU Cores', style={'color': '#FFFFFF'}),
                    dcc.Slider(
                        min=0,
                        max=24,
                        marks={i: '1'.format(i) if i == 1 else str(i) for i in range(1, 24)},
                        value=1,
                    ),
                    html.Div([
                        html.H6('OS Type', style={'color': '#FFFFFF'}),
                        html.Div([
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Windows', 'value': 'Windows'},
                                    {'label': 'Linux', 'value': 'Linux'},
                                    {'label': 'Other', 'value': 'Other'}
                                ],
                                value=''
                            ),
                        ], className="ten columns"),
                    ], className="row"),
                    html.H6('Disk size in GB', style={'color': '#FFFFFF'}),
                    html.Div(dcc.Input(id='input-box', type='number'), className="ten columns"),
                    # Form submission button
                    html.Div([
                        html.Button('Submit', id='button',
                                    style={'color': '#FFFFFF', 'backgroundColor': '#111111', "float": "right"}, className="five columns")
                    ], className="row")
                ])
            ], className="six columns", style={'backgroundColor': '#3d4e5c', 'padding': '10px'}),
            # Live remaining resources
            html.Div([
                html.H3('Remaining Resources', style={'color': '#111111'}),
                html.H5("RAM: " + str(round(avaliable_resources('memory'), 2)) + " GB remaining"),
                html.H5("Storage: " + str(round(remaining_storage(), 2)) + " GB remaining"),
            ], className="six columns", style={'backgroundColor': '#e8f4f7', 'padding': '10px', 'text-align':'center'})
        ], className='row')

# Retrieve virtual machine information from database
def virtualMachines(appliance, id):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Virtual_Machines"]
    mycol = mydb["Machines"]
    try:
        for vm in mycol.find({"id" : id}):
           # print(vm)
            results = vm
            del results['_id']
            vm_name = results[appliance]
            return vm_name
    except:
        vm_name = '0'
        return vm_name


# Retrieve system information from database
def systemSpecs(value):
    try:
        component = []
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["System_Specs"]
        mycol = mydb["Specs"]

        results = mycol.find({"_id": 0})
        for info in results:
            info.pop('_id')
            for specs in info:
                component.append(info[specs])
            return str(component[value])
    except:
        return "Failed to retrieve data"


# Select coresponding piece of hardware to retrieve from database
def cpu_cores():
    return systemSpecs(0)


def cpu_sockets():
    return systemSpecs(1)


def cpu_threads():
    return systemSpecs(2)


def cpu_mhz():
    return systemSpecs(3)


def cpu_model():
    return systemSpecs(4)


def memory_size():
    return round(float(systemSpecs(5)) / 2**30, 2)


def vendor():
    return systemSpecs(6)


def model():
    return systemSpecs(7)


def server_IP():
    return systemSpecs(8)


def vcenter_IP():
    return systemSpecs(9)


def network_interfaces():
    return systemSpecs(10)


def remaining_storage():
    return round(float(systemSpecs(11)) /2**30, 2)


def total_storage():
    return round(float(systemSpecs(12)) /2**30, 2)


# Calaculate remaining resources of system
def avaliable_resources(value):
        vm_usage = float(get_data(10)) / 1024
        print(vm_usage)
        total_system_memory = float(systemSpecs(5)) / 1024**3
        print(total_system_memory )
        remaining = total_system_memory- vm_usage
        print(remaining)
        return remaining

# Retrieve storage or memory usage
def get_data(value):
    try:
        component = []
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Virtual_Machines"]
        mycol = mydb["Machines"]

        results = mycol.find({})
        for info in results:
            info.pop('_id')
            for specs in info:
                component.append(info[specs])
            return str(component[8])
    except:
        return 0



if __name__ == '__main__':
    app.run_server(host="0.0.0.0")
