import qrcode

# Create an instance of the QRCode class
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Add data to the QRCode object and make it readable
data = 'https://frsecure.com/qr-code-scams/'
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QRCode object
img = qr.make_image(fill_color="black", back_color="white")

# Define the file path where the QR code will be saved
file_path = r"C:\Users\Win11User\Desktop\Randomcode\qrcodereal.png"

# Save the image to the specified file path
img.save(file_path)

# Print completion message
print("Job done. QR Code saved at:", file_path)

# Wait for user input before exiting
input("Press Enter to exit...")
