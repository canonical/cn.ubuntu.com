import intlTelInput from "intl-tel-input";

const phone = document.querySelector("#phone");

if (phone) {
  intlTelInput(phone, {
    initialCountry: "cn",
    separateDialCode: true,
    hiddenInput: () => ({ phone: "phone" }),
    loadUtils: () => import("intl-tel-input/utils"),
  });

  // Remove the visible input's name so only the hidden full-number field is
  // submitted (prevents a duplicate `phone` field).
  phone.removeAttribute("name");
}
