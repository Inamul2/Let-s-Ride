# let-s-ride

1st API : http://127.0.0.1:8000/rider/create/
- It adds a rider data to DB
input format :{
        "From": "Bangalore",
        "To": "Chennai",
        "dateandtime": "2022-12-19 15:30:00",
        "medium": "car", 
        "assets": "3"
    }

the mentioned keys should be present, 'dateandtime' key should have a value in "yyyy-mm-dd hh:mm:ss" format

outpu format : {
    "Status": "Success",
    "Message": "Rider data has been added successfully",
    "Rider Data": {
        "From": "Bangalore",
        "To": "Chennai",
        "dateandtime": "2022-12-19 15:30:00",
        "medium": "car",
        "assets": 3
    }
}




2nd API : http://127.0.0.1:8000/requester/request/
- it will add requester data to DB

input format : {
	"From": "Kolkata",
	"To": "Hyderabad",
	"dateandtime": "2022-12-09 15:30:00", # should have a value in "yyyy-mm-dd hh:mm:ss" format
	"assets": "3",
	"asset_type": "laptop", #should have a value between 'laptop', 'package', 'travel bag'
	"asset_sensitivity": "sensitive" # should have a value between 'highly sensitive', 'sensitive', 'normal'
}

output format : 
{
    "Status": "Success",
    "Message": "Your Request has been added successfully",
    "Request": {
        "From": "Kolkata",
        "To": "Hyderabad",
        "dateandtime": "2022-12-09 15:30:00",
        "assets": 3,
        "asset_type": "laptop",
        "asset_sensitivity": "sensitive"
    }
}





3rd API : http://127.0.0.1:8000/requester/getRequests/
- it can sort the data in datetime format , ascending or descending , and filter with status as pending or expired

input can be empty in this case, also it can take "sort" key with a value of "ASC" or "DESC", or/and "status" key with a value of "pending" or "expired"
input formats : 1 - {}
2 - {
	"sort": "ASC",
	"status": "pending"
}

3 - {
	"sort": "ASC"
  }

4 - {
	"status": "pending"
}

output : {
    "Status": "Success",
    "Message": "List of Requests retrieved Successfully",
    "Requests": [
        {
            "ID": 1,
            "From": "Kolkata",
            "To": "Hyderabad",
            "dateandtime": "2022-12-09 15:30:00",
            "assets": 3,
            "asset_type": "laptop",
            "asset_sensitivity": "sensitive",
            "status": "pending",
            "applied": "Applied"
        },
        {
            "ID": 9,
            "From": "Kolkata",
            "To": "Hyderabad",
            "dateandtime": "2022-12-09 15:30:00",
            "assets": 3,
            "asset_type": "laptop",
            "asset_sensitivity": "sensitive",
            "status": "pending",
            "applied": "Not Applied"
        },
        {
            "ID": 4,
            "From": "Kolkata",
            "To": "Noida",
            "dateandtime": "2022-12-11 15:30:00",
            "assets": 10,
            "asset_type": "travel bag",
            "asset_sensitivity": "highly sensitive",
            "status": "pending",
            "applied": "Not Applied"
        },
        {
            "ID": 8,
            "From": "Gurgaon",
            "To": "Mumbai",
            "dateandtime": "2022-12-25 20:00:00",
            "assets": 3,
            "asset_type": "laptop",
            "asset_sensitivity": "highly sensitive",
            "status": "pending",
            "applied": "Not Applied"
        },
        {
            "ID": 6,
            "From": "Goa",
            "To": "Haryana",
            "dateandtime": "2023-01-10 20:30:00",
            "assets": 8,
            "asset_type": "laptop",
            "asset_sensitivity": "normal",
            "status": "pending",
            "applied": "Applied"
        }
    ]
}




4th API : http://127.0.0.1:8000/requester/getMatchedRequests/
- it will give ut all the matched requesters data

it doesn't take any input

output : {
    "Status": "Success",
    "Message": "List of all Matched Requests retrieved Successfully",
    "Requests": [
        {
            "ID": 1,
            "From": "Kolkata",
            "To": "Hyderabad",
            "dateandtime": "2022-12-09 15:30:00",
            "assets": 3,
            "asset_type": "laptop",
            "asset_sensitivity": "sensitive",
            "status": "pending",
            "applied": "Applied"
        },
        {
            "ID": 9,
            "From": "Kolkata",
            "To": "Hyderabad",
            "dateandtime": "2022-12-09 15:30:00",
            "assets": 3,
            "asset_type": "laptop",
            "asset_sensitivity": "sensitive",
            "status": "pending",
            "applied": "Not Applied"
        },
        {
            "ID": 6,
            "From": "Goa",
            "To": "Haryana",
            "dateandtime": "2023-01-10 20:30:00",
            "assets": 8,
            "asset_type": "laptop",
            "asset_sensitivity": "normal",
            "status": "pending",
            "applied": "Applied"
        },
        {
            "ID": 8,
            "From": "Gurgaon",
            "To": "Mumbai",
            "dateandtime": "2022-12-25 20:00:00",
            "assets": 3,
            "asset_type": "laptop",
            "asset_sensitivity": "highly sensitive",
            "status": "pending",
            "applied": "Not Applied"
        }
    ]
}



5th API : http://127.0.0.1:8000/requester/apply/
- the API will apply for the rider info
- it will take details of the requet in order to apply

input format : {
            "From": "Gurgaon",
            "To": "Mumbai",
            "dateandtime": "2022-12-25 20:00:00",
            "assets": "3",
            "asset_type": "laptop",
            "asset_sensitivity": "highly sensitive"
        }
        
        
output format : {
    "Status": "Success",
    "Message": "You have applied for your request successfully",
    "Request": {
        "ID": 8,
        "From": "Gurgaon",
        "To": "Mumbai",
        "dateandtime": "2022-12-25 20:00:00",
        "assets": 3,
        "asset_type": "laptop",
        "asset_sensitivity": "highly sensitive",
        "status": "pending",
        "applied": "Applied"
    }
}

