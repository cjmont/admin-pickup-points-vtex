# Odoo AddPickupPoints Module README

## Overview

This module defines a model called `AddPickupPoints` in Odoo to manage the details of different pickup points for a store. It provides an interface to add, update, and send this information to VTEX, an e-commerce platform.

## Dependencies

- `Odoo`: The module is designed to work in an Odoo environment.
- `pytz`: For time zone management.
- `requests`: For HTTP calls.

## Model Structure

### Fields

- `store_id`: Store identification number (Integer, Required, Max length: 10)
- `store_name`: Store name (Char, Optional)
- `store_description`: URL for the store image (Char, Optional)
- ... (Additional fields for address, business hours, etc.)

### Business Logic

- `send_to_vtex()`: Method to send data to VTEX via API calls.
- `create()`: Odoo ORM method overridden to send data after creation.
- `write()`: Odoo ORM method overridden to send data after updates.
- `_compute_store_image()`: Method to convert the URL to a binary image.

## Usage

1. Create a new record by providing values for the fields.
2. Save the record. The `create()` method will automatically send this data to VTEX.
3. Update the record if needed. The `write()` method will send updated data to VTEX.

## Error Handling

- Logs errors when the API call to VTEX fails.
- Provides detailed traceback information for debugging.

## Installation

1. Download or clone the module.
2. Place it in the Odoo addons directory.
3. Update the Odoo app list and install the module.

## Configuration

You may need to provide valid API keys (`X-VTEX-API-AppKey` and `X-VTEX-API-AppToken`) in the `send_to_vtex()` method for successful API calls to VTEX.

```python
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-VTEX-API-AppKey': '<YOUR_APP_KEY>',
    'X-VTEX-API-AppToken': '<YOUR_APP_TOKEN>'
}
```

## Support

For any issues, questions, or contributions, please contact the maintainer.

## License

The module is licensed under [license_name].

---

Feel free to improve or extend this README as needed for your project.