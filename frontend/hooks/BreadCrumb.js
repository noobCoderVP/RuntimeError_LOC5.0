import React from "react";

export function BreadCrumb(URL) {
    const segments = URL.split("/");
    let finals = [];
    finals.push("Home");
    for (let i of segments) {
        if (i.indexOf(":") == -1 && i != "") finals.push(i);
    }

    finals = finals.map((element, index) => (
        <span key={index} className="dark:text-white text-black">
            {element}
        </span>
    ));
    return finals;
}
