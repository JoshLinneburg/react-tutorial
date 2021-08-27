import { Field, Form, Formik } from "formik";
import React from "react";

export default function EditUserForm({ user, onSubmit }) {
  return (
    <Formik
      initialValues={{
        firstName: user.first_name,
        lastName: user.last_name,
        email: user.email,
        phoneNumber: user.phone_nbr,
      }}
      onSubmit={onSubmit}
    >
      {() => (
        <Form>
          <div>
            <label htmlFor={"firstName"}>First Name</label>
            <Field id="firstName" type="text" name="firstName" />
          </div>
          <div>
            <label htmlFor={"lastName"}>Last Name</label>
            <Field id="lastName" type="text" name="lastName" />
          </div>
          <div>
            <label htmlFor={"email"}>Email</label>
            <Field id="email" type="text" name="email" />
          </div>
          <div>
            <label htmlFor={"phoneNumber"}>Phone Number</label>
            <Field id="phoneNumber" type="text" name="phoneNumber" />
          </div>
          <button type="submit">Update Profile</button>
        </Form>
      )}
    </Formik>
  );
}
