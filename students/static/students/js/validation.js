document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("studentForm");

    if (!form) return;

    form.addEventListener("submit", function (e) {

        e.preventDefault();

        const name = document.querySelector("[name='name']").value.trim();
        const email = document.querySelector("[name='email']").value.trim();
        const phone = document.querySelector("[name='phone']").value.trim();
        const parentContact = document.querySelector("[name='parent_contact']").value.trim();
        const pincode = document.querySelector("[name='pincode']").value.trim();

        const obtained = parseInt(
            document.querySelector("[name='obtained_marks']").value || 0
        );

        const total = parseInt(
            document.querySelector("[name='total_marks']").value || 0
        );

        // Name Validation
        if (name.length < 3) {
            Swal.fire({
                icon: "error",
                title: "Invalid Name",
                text: "Name must be at least 3 characters long"
            });
            return;
        }

        // Email Validation
        if (email !== "") {

            const emailPattern =
                /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!emailPattern.test(email)) {
                Swal.fire({
                    icon: "error",
                    title: "Invalid Email",
                    text: "Please enter a valid email address"
                });
                return;
            }
        }

        // Phone Validation
        if (phone !== "" && !/^\d{10}$/.test(phone)) {
            Swal.fire({
                icon: "error",
                title: "Invalid Phone Number",
                text: "Phone number must be exactly 10 digits"
            });
            return;
        }

        const gender = document.querySelector("[name='gender']").value;

        if (gender === "") {
            Swal.fire({
                icon: "error",
                title: "Gender Required",
                text: "Please select gender"
            });
            return;
        }

        // Parent Contact Validation
        if (
            parentContact !== "" &&
            !/^\d{10}$/.test(parentContact)
        ) {
            Swal.fire({
                icon: "error",
                title: "Invalid Parent Contact",
                text: "Parent contact must be exactly 10 digits"
            });
            return;
        }

        // Pincode Validation
        if (
            pincode !== "" &&
            !/^\d{6}$/.test(pincode)
        ) {
            Swal.fire({
                icon: "error",
                title: "Invalid Pincode",
                text: "Pincode must be exactly 6 digits"
            });
            return;
        }

        // Marks Validation
        if (obtained > total && total > 0) {
            Swal.fire({
                icon: "error",
                title: "Invalid Marks",
                text: "Obtained marks cannot be greater than total marks"
            });
            return;
        }

        // Confirm Save/Update
        Swal.fire({
            title: "Confirm",
            text: "Do you want to save student details?",
            icon: "question",
            showCancelButton: true,
            confirmButtonText: "Yes",
            cancelButtonText: "Cancel",
            confirmButtonColor: "#0d6efd"
        }).then((result) => {

            if (result.isConfirmed) {
                HTMLFormElement.prototype.submit.call(form);
            }

        });

    });

});