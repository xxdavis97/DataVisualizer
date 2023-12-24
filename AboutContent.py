import dash_core_components as dcc
import dash_html_components as html


ABOUT_CONTENT = html.Div(children= [
    html.Div(children = [
        html.Div(id="selfie", className="six columns", children = [
            html.Img(src="/assets/me.png", className="myBioPic"),
            html.Div(className="about", children=[
                html.H2("About", className="aboutHeader"),
                html.P("Jared graduated from Stevens Institute of Technology in 2020 with a Bachelor of Science for Computer Science in "
                       "addition to double minoring in Quantitative Finance as well as Pure & Applied Mathematics.  After graduation "
                       "Jared started his career at Goldman Sachs where he is a Software Engineer for Goldman Sachs Asset Management as part of the External Investing Group.  "
                       "Outside of work, Jared enjoys to work on coding side projects such as this website.  Some "
                       "of Jared's non-coding related interests include travelling, skiing, golfing and reading.  ")
            ])
        ]),
        html.Div(id="skills", className="six columns", children = [
            html.Div(className="skills", children=[
                html.H2("Core Skills And Abilities", className="aboutHeader"),
                html.Ul(children=[
                    html.Li(
                        "Programming experience in Python, Java, JavaScript, SQL, C#, Git, Angular, Neo4j, HTML, CSS"),
                    html.Li(
                        "Well versed in popular Python libraries such as Numpy, Pandas, Matplotlib, Requests, Beautiful Soup, Pyodbc, "
                        "Selenium, Xlwings, Flask and Dash (the library used to create this site)"),
                    html.Li(
                        "Experienced in Java frameworks/libraries such as Spring, MyBatis, Hibernate, Dropwizard, Jackson"),
                    html.Li(
                        "As a side project developed a trend following stock algorithm deployed on a raspberry pi server that sends email "
                        "alerts of potential stock picks."),
                    html.Li(
                        "A second side project was the development of this website, which uses Python, notably Dash, Flask, Numpy, Pandas, "
                        "Requests, and Beautiful Soup.  Version control is covered by Github and deployment by Azure")
                ])
            ])
        ]),
    ], className="row topRow aboutRow"),
    html.Br(),
    html.Div(className="row aboutRow", children=[
        html.H2("Work Experience", className="aboutHeader")
    ]),
    html.Div(className="row aboutRow workRow", children=[
        html.Div(className="workInput", children = [
            # html.H6("Goldman Sachs - New York, NY"),
            html.H6("Goldman Sachs — Software Engineer"),
            html.Div(className="aboutSubInfo", children= [
                html.P("200 West St. New York, NY"),
                html.P("May — August 2019, July 2020 — Present"),
            ]),
            html.Ul(children=[
                html.Li(
                    "Wrote an application utilizing Angular, Java, and SQL to allow the business to gain streamlined"
                    " visibility of critical missing data for our private equity investments, allowing for easy correction."),
                html.Li(
                    "Worked closely with data providers and business stakeholders to develop an application to automate the screening of ETF data based on various proprietary rules.  Following the "
                    "screen the system automatically uploads various reports to ultimately inform client investing decisions."),
                html.Li("Created a system to automate the generation of Investment Committee as well as client materials by pulling from various third-party data sources in conjunction with internal proprietary data.  This"
                        "enhancement saved an estimated 10 hours of work per report, of which there are thousands of reports generated per annum."),
            ])
        ]),
    ]),
    html.Div(className="row aboutRow workRow", children=[
        html.Div(className="workInput", children=[
            # html.H6("Virtual Facility - New York, NY"),
            html.H6("Virtual Facility — Software Developer"),
            html.Div(className="aboutSubInfo", children=[
                html.P("39 West 37th St. New York, NY"),
                html.P("May — December 2018"),
            ]),
            # html.P("39 West 37th St. New York, NY", className='companyAddress'),
            # html.P("May-December 2018", className='datesWorked'),
            html.Ul(children=[
                html.Li("Modified production level web applications using the Angular JavaScript framework, powered and optimized "
                        "by a Neo4j Graph Database to allow for significantly improved performance over large datasets."),
                html.Li("Reporting to the CEO, headed the company’s switch to the Agile software development process using Atlassian’s JIRA."),
                html.Li("Created a dashboard for top-level management, as well as developers, to gain insight into "
                        "the velocity of our team.  This enabled much better project planning and led to a dramatic increase in efficiency."),
            ])
        ]),
    ]),
    html.Div(className="row aboutRow workRow", children=[
        html.Div(className="workInput", children=[
            #html.H6("Sphere Technology Solutions - Jersey City, NJ"),
            html.H6("Sphere Technology Solutions — Software Developer"),
            html.Div(className="aboutSubInfo", children=[
                html.P("525 Washington Blvd. Jersey City, NJ"),
                html.P("August — December 2017"),
            ]),
            # html.H6("Sphere Technology Solutions — Jersey City, NJ"),
            # html.P("525 Washington Blvd. Jersey City, NJ", className='companyAddress'),
            # html.P("August-December 2017", className='datesWorked'),
            html.Ul(children=[
                html.Li("Played a major role as a full stack developer towards development and maintenance of Sphere’s leading "
                        "product, SphereBoard."),
                html.Li("Generated interactive pages through the use of JavaScript/JQuery, HTML, and CSS, in addition to server-side "
                        "C# and SQL, that allowed clients to gain a more transparent view into the security of their infrastructure."),
                html.Li("Utilized Agile/Scrum software development framework to complete product releases efficiently within a team"),
                html.Li("Heavily worked with the model view controller web application design pattern, coupled with the ASP.NET "
                        "Web API framework, to develop features for high profile clients")
            ])
        ]),
    ]),
    html.Div(className="row aboutRow", children=[
        html.Div(className="workInput", children=[
            # html.H6("Brigade Capital Management - New York, NY"),
            html.H6("Brigade Capital Management — Software Developer"),
            html.Div(className="aboutSubInfo", children=[
                html.P("399 Park Ave. New York, NY"),
                html.P("January — May 2017"),
            ]),
            # html.H6("Brigade Capital Management — New York, NY"),
            # html.P("399 Park Ave. New York, NY", className='companyAddress'),
            # html.P("January-May 2017", className='datesWorked'),
            html.Ul(children=[
                html.Li("Developed scripts in python to manage and analyze large stores of investment data, including devising "
                        "a class to call any SQL query, procedure, or file directly from Python and store the result in a dataframe.  This "
                        "enabled Brigade to run Python’s powerful data analysis functions directly on its SQL databases."),
                html.Li("Created a python class featuring vectorized methods to prioritize execution speed.  "
                        "All functions were customized to be imported into MS Excel to facilitate comparisons of returns, or any other source of data, either with a normal distribution or with another dataset.  "
                        "This allowed people without coding know-how to leverage these powerful data analytics tools."),
                html.Li("Created automatic email alerts in SQL to notify traders of important price and metric movements in addition "
                        "to alerts showing daily, weekly, and monthly changes in a wide array of portfolio level risk statistics."),
                html.Li("Generated plugins to make Python analyses user friendly in MS Excel.")
            ])
        ]),
    ]),
    html.Br(),
    html.Div(className="row aboutRow", children=[
            html.H2("Contact Information", className="aboutHeader")
        ]),
    html.Div(className="row aboutRow", children=[
        html.Div(className="workInput contactList", children = [
            html.Ul(children=[
                html.Li(
                    "Cell: (845) 667-9413"),
                html.Li(
                    "Email: xxdavis97@gmail.com"),
                html.Li("Linkedin: https://www.linkedin.com/in/jared-d-bb0b5699/"),
            ])
        ]),
    ]),
    html.Br()
])