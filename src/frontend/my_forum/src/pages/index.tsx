import {} from "react-router";
import { createBrowserRouter } from "react-router-dom";
import { Layout } from "../components/layout";
import { CreateQuestionPage } from "./question/create.tsx";
import { ViewQuestionPage } from "./question/view.tsx";
import { ListQuestionPage } from "./question/list.tsx";
import { HomePage } from "./home.tsx";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "/question/create",
        element: <CreateQuestionPage />,
      },
      {
        path: "/question/:id",
        element: <ViewQuestionPage />,
      },
      {
        path: "/question",
        element: <ListQuestionPage />,
      },
    ],
  },
]);
