# Request Examples

## Invoices Endpoint

Endpoint: http://127.0.0.1:8000/get_data

Method: POST

```json
{
  "key": "aiwapi12345",
  "urls": [
    "https://res.cloudinary.com/gurukol/image/upload/v1688653962/aiw/frontPage/sample01_all7jg.jpg",
    "https://res.cloudinary.com/gurukol/image/upload/v1688654039/aiw/backPage/sample01_sqskxd.jpg"
  ]
}
```

<br/>

## Pan Card Endpoint

Endpoint: http://127.0.0.1:8000/get-pan-details

Method: POST

```json
{
  "key": "aiwapi12345",
  "url": "https://res.cloudinary.com/gurukol/image/upload/v1688979862/aiw/panCard/sanchit_pan_card_kaz91t.jpg"
}
```

<br/>

## Aadhar Card Endpoint

Endpoint: http://127.0.0.1:8000/get-aadhar-details

Method: POST

```json
{
  "key": "aiwapi12345",
  "url": "https://res.cloudinary.com/gurukol/image/upload/v1688660003/aiw/aadhar/aadhar03_yzyo13.jpg"
}
```
