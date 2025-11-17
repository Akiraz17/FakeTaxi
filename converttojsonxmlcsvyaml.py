import sqlite3
import json
import csv
import yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
from pathlib import Path

def retrievedatafromdb(db_path='database.db'):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()


        query = """
        SELECT
                r.ride_id,
                r.passenger_id,
                p.full_name as passenger_name,
                p.phone as passenger_phone,
                p.email as passenger_email,
                p.rating as passenger_rating,
                r.driver_id,
                d.full_name as driver_name,
                d.phone as driver_phone,
                d.email as driver_email,
                d.rating as driver_rating,
                d.balance as driver_balance,
                d.car_model,
                d.car_number,
                r.support_id,
                s.ticket,
                s.full_name as support_name,
                s.phone as support_phone,
                s.email as support_email,
                s.status as support_status,
                s.balance as support_balance,
                r.start_point,
                r.end_point,
                r.price,
                r.created_at,
                r.completed_at,
                r.status as ride_status
        FROM rides r
        LEFT JOIN passengers p ON r.passenger_id = p.passenger_id
        LEFT JOIN drivers d ON r.driver_id = d.driver_id
        LEFT JOIN support s ON r.support_id = s.support_id
        ORDER BY r.ride_id
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        conn.close()
        return data




def savejson(data):
    formatted_data = []
    for item in data:
        ride = {
                "passenger": {
                        "id": item["passenger_id"],
                        "passenger_full_name": item["passenger_name"],
                        "passenger_phone": item["passenger_phone"],
                        "passenger_email": item["passenger_email"],
                        "passenger_rating": item["passenger_rating"]
                } if item["passenger_id"] else None,
                "driver": {
                        "id": item["driver_id"],
                        "driver_full_name": item["driver_name"],
                        "driver_phone": item["driver_phone"],
                        "driver_email": item["driver_email"],
                        "driver_rating": item["driver_rating"],
                        "balance": item["driver_balance"],
                        "car": {
                                "car_model": item["car_model"],
                                "car_number": item["car_number"]
                        }
                } if item["driver_id"] else None,
                "support": {
                        "id": item["support_id"],
                        "ticket": {
                                "passenger_id": item["passenger_id"],
                                "driver_id": item["driver_id"]
                        },
                        "support_full_name": item["support_name"],
                        "support_phone": item["support_phone"],
                        "support_email": item["support_email"],
                        "support_status": item["support_status"],
                        "balance": item["support_balance"]
                } if item["support_id"] or (item["passenger_id"] and item["driver_id"]) else None,
                "route": {
                        "start": item["start_point"],
                        "end": item["end_point"]
                },
                "price": item["price"],
                "time": {
                        "created_at": item["created_at"],
                        "completed_at": item["completed_at"]
                },
                "status": item["ride_status"]
        }
        formatted_data.append(ride)

    os.makedirs('out', exist_ok=True)
    with open('out/data.json', 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=2)

def savecsv(data):
        if not data:
                return
        with open('out/data.csv', 'w', newline='', encoding='utf-8') as f:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(data)

def savexml(data):
        root = ET.Element("rides")

        for item in data:
                ride = ET.SubElement(root, "ride")

                ET.SubElement(ride, "ride_id").text = str(item["ride_id"])

                if item["passenger_id"]:
                        passenger = ET.SubElement(ride, "passenger")
                        ET.SubElement(passenger, "passenger_id").text = str(item["passenger_id"])
                        ET.SubElement(passenger, "full_name").text = item["passenger_name"]
                        ET.SubElement(passenger, "phone").text = item["passenger_phone"]
                        ET.SubElement(passenger, "email").text = item["passenger_email"]
                        ET.SubElement(passenger, "rating").text = str(item["passenger_rating"])

                if item["driver_id"]:
                        driver = ET.SubElement(ride, "driver")
                        ET.SubElement(driver, "driver_id").text = str(item["driver_id"])
                        ET.SubElement(driver, "full_name").text = item["driver_name"]
                        ET.SubElement(driver, "phone").text = item["driver_phone"]
                        ET.SubElement(driver, "email").text = item["driver_email"]
                        ET.SubElement(driver, "rating").text = str(item["driver_rating"])
                        ET.SubElement(driver, "balance").text = str(item["driver_balance"])
                        ET.SubElement(driver, "car_model").text = item["car_model"]
                        ET.SubElement(driver, "car_number").text = item["car_number"]

                if item["support_id"]:
                        support = ET.SubElement(ride, "support")
                        ET.SubElement(support, "support_id").text = str(item["support_id"])
                        ET.SubElement(support, "ticket").text = item["ticket"]
                        ET.SubElement(support, "passenger_id").text = str(item["passenger_id"])
                        ET.SubElement(support, "driver_id").text = str(item["driver_id"])
                        ET.SubElement(support, "full_name").text = item["support_name"]
                        ET.SubElement(support, "phone").text = item["support_phone"]
                        ET.SubElement(support, "email").text = item["support_email"]
                        ET.SubElement(support, "status").text = item["support_status"]
                        ET.SubElement(support, "balance").text = str(item["support_balance"])
                
                route = ET.SubElement(ride, "route")
                ET.SubElement(route, "start_point").text = item["start_point"]
                ET.SubElement(route, "end_point").text = item["end_point"]

                ET.SubElement(ride, "price").text = str(item["price"])
                ET.SubElement(ride, "created_at").text = item["created_at"]
                if item["completed_at"]:
                        ET.SubElement(ride, "completed_at").text = item["completed_at"]
                ET.SubElement(ride, "status").text = item["ride_status"]

                xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")

        with open('out/data.xml', 'w', encoding='utf-8') as f:
                f.write(xml_str)

def saveyaml(data):
        formatted_data = []
        for item in data:
                ride = {
                "passenger": {
                        "id": item["passenger_id"],
                        "passenger_full_name": item["passenger_name"],
                        "passenger_phone": item["passenger_phone"],
                        "passenger_email": item["passenger_email"],
                        "passenger_rating": item["passenger_rating"]
                } if item["passenger_id"] else None,
                "driver": {
                        "id": item["driver_id"],
                        "driver_full_name": item["driver_name"],
                        "driver_phone": item["driver_phone"],
                        "driver_email": item["driver_email"],
                        "driver_rating": item["driver_rating"],
                        "balance": item["driver_balance"],
                        "car": {
                                "car_model": item["car_model"],
                                "car_number": item["car_number"]
                        }
                } if item["driver_id"] else None,
                "support": {
                        "id": item["support_id"],
                        "ticket": {
                                "passenger_id": item["passenger_id"],
                                "driver_id": item["driver_id"]
                        },
                        "support_full_name": item["support_name"],
                        "support_phone": item["support_phone"],
                        "support_email": item["support_email"],
                        "support_status": item["support_status"],
                        "balance": item["support_balance"]
                } if item["support_id"] or (item["passenger_id"] and item["driver_id"]) else None,
                "route": {
                        "start": item["start_point"],
                        "end": item["end_point"]
                },
                "price": item["price"],
                "time": {
                        "created_at": item["created_at"],
                        "completed_at": item["completed_at"]
                },
                "status": item["ride_status"]
                }
                formatted_data.append(ride)
        with open('out/data.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(formatted_data, f,
                          allow_unicode=True,
                          default_flow_style=False,
                          sort_keys=False)





def main():

    data = importdatafromdb()
    
    if not data:
        print("В базе данных нет записей")
        return

    savejson(data)
    savecsv(data)
    savexml(data)
    saveyaml(data)

if __name__ == "__main__":
    main()