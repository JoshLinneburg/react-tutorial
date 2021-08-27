import axios from "axios";
import { useState, useEffect, useMemo } from "react";
import Table from "../components/UserTable";

export default function Home() {
  let [users, setUsers] = useState([]);
  let [status, setStatus] = useState("loading");
  const columns = useMemo(
    () => [
      {
        Header: "First Name",
        accessor: "first_name",
      },
      {
        Header: "Last Name",
        accessor: "last_name",
      },
      {
        Header: "Email",
        accessor: "email",
      },
      {
        Header: "Phone Number",
        accessor: "phone_nbr",
      },
      {
        Header: "Links",
        accessor: "public_id",
      },
    ],
    []
  );

  useEffect(() => {
    async function getData() {
      try {
        let response = await axios.get("/api/v1/user");
        setUsers(response.data.body);
        setStatus("success");
      } catch (error) {
        setStatus("error");
        console.error(error);
      }
    }
    if (status === "loading") {
      getData();
    }
  }, []);

  return (
    <div>
      {status === "success" ? (
        <>
          <Table columns={columns} data={users} />
        </>
      ) : (
        "Loading..."
      )}
    </div>
  );
}
