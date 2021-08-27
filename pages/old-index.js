import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";
import { Formik, Form, Field } from "formik";
import Link from "next/link";
import { UserPage } from "./user/[publicId]";

function FormikNameForm({ user, onSubmit }) {
  return (
    <Formik
      initialValues={{ firstName: user.first_name, lastName: user.last_name }}
      onSubmit={onSubmit}
    >
      {({ isSubmitting }) => (
        <Form>
          <Field type="text" name="firstName" />
          <Field type="text" name="lastName" />
          <button type="submit" disabled={isSubmitting}>
            Submit
          </button>
        </Form>
      )}
    </Formik>
  );
}

function NameForm({ user, handleSubmit, setUser }) {
  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor={"firstName"}>First Name</label>
        <input
          value={user.first_name}
          onChange={(event) => {
            setUser({ ...user, first_name: event.target.value }); // What is this "..." operator?
          }}
          id={"firstName"}
        />
      </div>
      <div>
        <label htmlFor={"lastName"}>Last Name</label>
        <input
          value={user.last_name}
          onChange={(event) => {
            setUser({ ...user, last_name: event.target.value }); // What is this "..." operator?
          }}
          id={"lastName"}
        />
      </div>
      <button type={"submit"}>Submit</button>
    </form>
  );
}

export default function Home() {
  let [user, setUser] = useState({});
  let [status, setStatus] = useState("loading");

  useEffect(() => {
    axios
      .get("/api/v1/user")
      .then((response) => {
        setUser(response.data.body);
        setStatus("success");
        console.log(response.data.body);
      })
      .catch((error) => {
        setStatus("error");
        console.error(error);
      });
  }, []);

  function handleSubmit(event) {
    console.log("Submitted!");
    event.preventDefault();

    let body = { first_name: user.first_name, last_name: user.last_name };
    axios
      .patch("/api/v1/user/e159f68e-eb6c-4632-aa4d-374076da32dd", body)
      .then((response) => {
        setUser(response.data.body);
      });
    // fetch("/api/v1/user/727b6004-b0dc-4904-b1f4-4f3c316d96a4", {
    //   method: "PATCH",
    //   headers: { "content-type": "application/json" },
    //   body: JSON.stringify(body),
    // }).then(async (response) => {
    //   await setUserFromResponse(response, setUser);
    // });
  }

  async function handleFormikSubmit(values, { setSubmitting }) {
    let body = { first_name: values.firstName, last_name: values.lastName };
    try {
      let response = await axios.patch(
        "/api/v1/user/e159f68e-eb6c-4632-aa4d-374076da32dd",
        body
      );
      setUser(response.data.data);
    } catch {
      console.error("Something went wrong!");
    }
    setSubmitting(false);
  }

  return (
    <div>
      <pre>{JSON.stringify(user, null, 2)}</pre>
      {status === "success" ? (
        <>
          <NameForm user={user} handleSubmit={handleSubmit} setUser={setUser} />
          <FormikNameForm user={user} onSubmit={handleFormikSubmit} />
        </>
      ) : (
        "Loading..."
      )}
    </div>
  );
}
