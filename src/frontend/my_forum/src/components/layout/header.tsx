import {
  Header as MantineHeader,
  Autocomplete,
  Group,
  Burger,
  Box,
  Avatar,
  Container,
} from "@mantine/core";
import { Button } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { IconSearch } from "@tabler/icons-react";
import { useNavigate } from "react-router-dom";
import logo from '../../assets/logo.png'
export function Header() {
  const navigate = useNavigate();
  const [opened, { toggle }] = useDisclosure(false);
  const loggedInUserJSON = localStorage.getItem("user");
  const loggedInUser = JSON.parse(loggedInUserJSON);

  const loggedInUsername = loggedInUser ? loggedInUser.fields.username : null;

  const handleLogout = () => {

    localStorage.removeItem("user");
    localStorage.removeItem("threads")
   
    navigate("/signin"); 
  };
  const handleHomePage = () =>{
    navigate("/");
  }

  return (
    <MantineHeader height={56} mb={120}>
      <Container size="xl" p="xs">
        <Group>
          <Group onClick={handleHomePage}>
            <Burger opened={opened} onClick={toggle} size="sm"  />
            <img className="w-[90px] h-[55px] mt-[-10px] cursor-pointer" src={logo} alt="Logo" />
          </Group>
          <Group sx={{ flexGrow: 1, justifyContent: "center" }} align="center">
            <Autocomplete
              sx={{ width: 600 }}
              placeholder="Search"
              icon={<IconSearch size="1rem" stroke={1.5} />}
              data={[
                "React",
                "Angular",
                "Vue",
                "Next.js",
                "Riot.js",
                "Svelte",
                "Blitz.js",
              ]}
            />
          </Group>
          <Box>
            {loggedInUsername ? (
              <div className="flex items-center">
                <Avatar
                className="cursor-pointer"
                  color="cyan"
                  radius="xl"
                  onClick={() => navigate("/account")}
                ></Avatar>
                <p className="ml-2">{loggedInUsername}</p>
                <Button
                  onClick={handleLogout}
                  className="ml-2 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
                >
                  Logout
                </Button>
              </div>
            ) : (
              <Button onClick={() => navigate("/signin")}>Login</Button>
            )}
          </Box>
        </Group>
      </Container>
    </MantineHeader>
  );
}

