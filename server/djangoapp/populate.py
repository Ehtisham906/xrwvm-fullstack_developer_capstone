def initiate():
    print("Running the populate script...")

    try:
        # CarMake data
        car_make_data = [
            {"name": "NISSAN", "description": "Great cars. Japanese technology"},
            {"name": "Mercedes", "description": "Great cars. German technology"},
            {"name": "Audi", "description": "Great cars. German technology"},
            {"name": "Kia", "description": "Great cars. Korean technology"},
            {"name": "Toyota", "description": "Great cars. Japanese technology"},
        ]

        car_make_instances = [
            CarMake.objects.create(name=data['name'], description=data['description'])
            for data in car_make_data
        ]

        # CarModel data
        car_model_data = [
            {"name": "Pathfinder", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": 1},
            {"name": "Qashqai", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": 2},
            {"name": "XTRAIL", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": 3},
            {"name": "A-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1], "dealer_id": 4},
            {"name": "C-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1], "dealer_id": 5},
        ]

        for data in car_model_data:
            CarModel.objects.create(
                name=data['name'],
                car_make=data['car_make'],
                type=data['type'],
                year=data['year'],
                dealer_id=data['dealer_id']
            )
            print(f"Created CarModel: {data['name']}")

        print("Data population completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
