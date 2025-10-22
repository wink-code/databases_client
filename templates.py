# This is the seletion query expression strings templages

class influx_template:
    query1 = '''from (bucket: "{bucket}")
            |> range(start: "{start}", stop: "{stop}")
            |> filter(fn: (r)=>
                r._measurement == "{measurement_name}" and 
                r._field == "{field}")
            '''
    query2 = '''from (bucket: "{bucket}")
            |> range(start: {start}, stop: {stop})
            |> filter(fn: (r)=>
                r._measurement == "{measurement_name}" and 
                r._field == "{field}")
            '''