import axios from "axios";
import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import EditProfileForm from "components/EditUserForm";
import UserProfile from "components/UserProfile";
import { api, createServerSideApiClient } from "lib/api";

export default function UserPage({ initialUser, initialStatus }) {
  const router = useRouter();
  const { publicId, editing } = router.query;
  let [user, setUser] = useState(initialUser);
  let [status, setStatus] = useState(initialStatus);
  let [isEditing, setIsEditing] = useState(editing === "true");

  useEffect(() => {
    async function getData() {
      try {
        let user = await api.getUserById(publicId);
        setUser(user);
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

  async function handleFormikSubmit(values, { setSubmitting }) {
    let body = {
      first_name: values.firstName,
      last_name: values.lastName,
      email: values.email,
      phone_nbr: values.phoneNumber,
    };
    try {
      let response = await axios.patch(`/api/v1/user/${user.public_id}`, body);
      setUser(response.data.body);
    } catch (error) {
      console.error("Something went wrong!");
      console.error(error);
    }
    setSubmitting(false);
  }

  return (
    <div>
      <button onClick={() => setIsEditing(!isEditing)}>
        Switch to {isEditing ? "Viewing" : "Editing"} Mode
      </button>
      <div>
        {status === "success" ? (
          isEditing ? (
            <EditProfileForm user={user} onSubmit={handleFormikSubmit} />
          ) : (
            <UserProfile user={user} />
          )
        ) : (
          "Loading..."
        )}
      </div>
    </div>
  );
}

// Why do I need this if I want the UserPage to return data on page refreshes?
export async function getServerSideProps({ query }) {
  let apiClient = createServerSideApiClient();
  try {
    let user = await apiClient.getUserById(query.publicId);
    return {
      props: {
        initialUser: user,
        initialStatus: "success",
      },
    };
  } catch (error) {
    console.error(error);
    return {
      props: {
        initialUser: null,
        initialStatus: "error",
      },
    };
  }
}
